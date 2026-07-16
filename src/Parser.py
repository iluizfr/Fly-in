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
        pre_check: list[str] = value.split()

        try:
            n = int(pre_check[1])
        except Exception:
            raise ParserError("Hubprocessor: ' ' not allowed in names of hub's")

        name = pre_check[0]
        x = pre_check[1]
        y = pre_check[2]
        meta_data: str = ""
        meta_data += " ".join(pre_check[3:])

        if "-" in name:
            raise ValueError(f"HubProcessor: '-' not allowed in names of hub's")
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
        self._ln = 1
        self.nb_drones: int = 0
        self.start_hub = None
        self.hubs: list[Hub] = []
        self.end_hub = None
        self.connections: list[Connection] = []
        self.set_config()

    def set_config(self) -> None:
        stack_keys: list[str] = []
        valid_keys: dict[str, Any] = {"nb_drones": NumericProcessor(),
                  "start_hub": HubProcessor(),
                  "hub": HubProcessor(),
                  "end_hub": HubProcessor(),
                  "connection": ConnectionProcessor()}

        with open(self.file_name, "r") as file:

            for line in file:

                line = line.strip()
                if not line or line.startswith("#"):
                    self._ln += 1
                    continue

                elif ":" not in line:
                    raise ParserError(f"Syntax: {self.file_name} line {self._ln} missing ':'")

                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()

                if key not in valid_keys.keys():
                    raise ParserError(f"Unknown key in {self.file_name} at line {self._ln}")

                if key in stack_keys:
                    raise ParserError(f"Duplicated key: {key} in line: {self._ln}")

                stack_keys.append(key)

                if key == "hub" or key == "connection":
                    stack_keys.remove(key)

                if key == "nb_drones":
                    if self.start_hub is not None or len(self.hubs) != 0 \
                        or self.end_hub is not None \
                        or len(self.connections) != 0:
                        raise ParserError("nb_drones not in first line")
                    config = valid_keys[key].converter(value)
                    self.nb_drones = config

                elif key == "start_hub":
                    if self.start_hub != None:
                        raise ParserError(f"Duplicate start_hub in line {self._ln}")
                    else:
                        config = valid_keys[key].converter(value)
                        self.start_hub = Hub(config["name"], config["coordinate"], config["meta_data"])

                elif key == "hub":
                    config = valid_keys[key].converter(value)
                    self.hubs.append(Hub(config["name"], config["coordinate"], config["meta_data"]))

                elif key == "end_hub":
                    if self.end_hub != None:
                        raise ParserError(f"Duplicate end_hub in line {self._ln}")
                    else:
                        config = valid_keys[key].converter(value)
                        self.end_hub = Hub(config["name"], config["coordinate"], config["meta_data"])

                elif key == "connection":
                    config = valid_keys[key].converter(value)
                    if "meta_data" in config:
                        self.connections.append(
                            Connection(config["connections"], config["meta_data"]))
                    else:
                        self.connections.append(Connection(config["connections"]))

                self._ln += 1

            self.__check_hubs_names()
            self.__check_hubs_coordinates()
            self.__check_connections()

    def __check_hubs_names(self) -> None:
        stack_names: list[str] = []
        stack_names.append(self.start_hub.name)
        stack_names.append(self.end_hub.name)

        if self.start_hub.name == self.end_hub.name:
            raise ParserError(f"Hub with duplicated name: {self.start_hub.name}")

        for hub in self.hubs:
            if hub.name in stack_names:
                raise ParserError(f"Hub with duplicated name: {hub.name}")
            stack_names.append(hub.name)

    def __check_hubs_coordinates(self) -> None:
        stack_coordinate: list[tuple[int, int]] = []
        stack_coordinate.append(self.start_hub.pos)
        stack_coordinate.append(self.end_hub.pos)

        if self.start_hub.pos == self.end_hub.pos:
            raise ParserError(f"Hub duplicated coordinate: {self.end_hub.pos}")

        for hub in self.hubs:
            if hub.pos in stack_coordinate:
                raise ParserError(f"Hub with duplicated coordinate: {hub.pos}")
            stack_coordinate.append(hub.pos)

    def __check_connections(self) -> None:
        previus_connections = []
        previus_reverse_connections = []
        hubs_names: list[str] = []

        hubs_names = [hub.name for hub in self.hubs]
        hubs_names.append(self.start_hub.name)
        hubs_names.append(self.end_hub.name)

        for c in self.connections:
            a, b = c.connection

            if a not in hubs_names:
                raise ParserError(f"Connection: {a} not in hubs names")
            if b not in hubs_names:
                raise ParserError(f"Connection: {b} not in hubs names")


            if c.connection in previus_connections \
                or c.connection in previus_reverse_connections:
                raise ParserError(f"Duplicated connection: {c.connection}")

            previus_connections.append(tuple((a, b)))
            previus_reverse_connections.append(tuple((b, a)))

    def display_parser(self) -> None:
        print(f"nb_drone: {self.nb_drones}\n")
        print("start_hub:")
        print(f"    name: {self.start_hub.name}")
        print(f"    pos: {self.start_hub.pos}")
        print(f"    meta data: {self.start_hub.meta_data}\n")

        print("Hubs:")
        for hub in self.hubs:
            print(f"    name: {hub.name}")
            print(f"    pos: {hub.pos}")
            print(f"    meta data: {hub.meta_data}\n")

        print("end_hub:")
        print(f"    name: {self.end_hub.name}")
        print(f"    pos: {self.end_hub.pos}")
        print(f"    meta data: {self.end_hub.meta_data}\n")

        print("Connections:")
        for connection in self.connections:
            print(f"    Connection: {connection.connection}")
            print(f"    meta data: {connection.meta_data}\n")
