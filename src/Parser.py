from abc import ABC, abstractmethod
from .Connection import Connection
from typing import Any
from .Hub import Hub


class Processor(ABC):
    @abstractmethod
    def converter(self, value: str) -> Any:
        pass


class NumericProcessor(Processor):
    def converter(self, value: str) -> int:
        return self.validate(value)

    @staticmethod
    def validate(value: str) -> int:
        new_value = int(value)
        if new_value < 0:
            raise ValueError("Parsing: No negative nb_drones allowed")
        return new_value


class HubProcessor(Processor):
    def converter(self, value: str) -> Any:
        hub: dict[str, Any] = {}

        name, x, y, meta_data = value.split(" ", 3)
        hub["name"] = name
        hub["coordinate"] = tuple((int(x), int(y)))
        hub["meta_data"] = meta_data

        return hub


class ConnectionProcessor(Processor):
    def converter(self, value: str) -> str:
        connection: dict[str, Any] = {}

        if "-" not in value:
            raise ValueError(f"Missing '-' in connection: {value}")

        word_count = len(value.split())

        if word_count == 1:
            a, b = value.split("-")
            connection["connections"] = tuple((a, b))

        elif word_count == 2:
            left, right = value.split(" ")
            a, b = left.split("-")
            connection["connections"] = tuple((a, b))
            connection["meta_data"] = right

        return connection


class ParserError(Exception):
    pass


class Parser:
    def __init__(self, file_name: str) -> None:
        self.file_name: str = file_name
        self.nb_drones = 0
        self.start_hub = None
        self.hubs: list[Hub] = []
        self.end_hub = None
        self.connections: List[Connection] = []
        self.set_config()


    def set_config(self) -> None:
        valid_keys = {"nb_drones": NumericProcessor(),
                  "start_hub": HubProcessor(),
                  "hub": HubProcessor(),
                  "end_hub": HubProcessor(),
                  "connection": ConnectionProcessor()}

        with open(self.file_name, "r") as file:
            ln = 1

            for line in file:

                line = line.strip()
                if not line or line.startswith("#"):
                    ln += 1
                    continue

                elif ":" not in line:
                    raise ParserError(f"Syntax: {self.file_name} line {ln} missing ':'")

                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()

                if key not in valid_keys.keys():
                    raise ParserError(f"Unknown key in {self.file_name} at line {ln}")

                if key == "nb_drones":
                    config = valid_keys[key].converter(value)
                    self.nb_drones = config

                elif key == "start_hub":
                    if self.start_hub != None:
                        raise ParserError(f"Duplicate start_hub in line {ln}")
                    else:
                        config = valid_keys[key].converter(value)
                        self.start_hub = Hub(config["name"], config["coordinate"], config["meta_data"])

                elif key == "hub":
                    config = valid_keys[key].converter(value)
                    self.hubs.append(Hub(config["name"], config["coordinate"], config["meta_data"]))

                elif key == "end_hub":
                    if self.end_hub != None:
                        raise ParserError(f"Duplicate end_hub in line {ln}")
                    else:
                        config = valid_keys[key].converter(value)
                        self.end_hub = Hub(config["name"], config["coordinate"], config["meta_data"])

                elif key == "connection":
                    config = valid_keys[key].converter(value)
                    if "meta_data" in config:
                        self.connections.append(Connection(config["connections"], config["meta_data"]))
                    else:
                        self.connections.append(Connection(config["connections"]))

                ln += 1


    def __verify_config(self, config: dict[str, Any]) -> list[Any]:
        erros: list[str] = []
        keys = ["nb_drones", "start_hub", "hub", "end_hub", "connection"]

        for key in config.keys():
            if key in keys:
                keys.remove(key)

        for key in keys:
            erros.append(f"Missing key: {key}")

        if len(erros) > 0:
            return erros
        else:
            return 0
