from abc import ABC, abstractmethod
from typing import Any


class Processor(ABC):
    @abstractmethod
    def converter(self, value: str) -> Any:
        pass

    @staticmethod
    def validate(value: str) -> int:
        new_value = int(value)
        if new_value < 0:
            raise ValueError("Parsing: No Negative numbers allowed")
        return new_value


class NumericProcessor(Processor):
    def converter(self, value: str) -> int:
        return self.validate(value)


class HubProcessor(Processor):
    def converter(self, value: str) -> Any:
        hub: dict[str, Any] = {}

        name, x, y, meta_data = value.split(" ", 3)
        hub["name"] = name
        hub["coordenate"] = tuple((int(x), int(y)))
        hub["meta_data"] = meta_data

        return hub


class ConnectionProcessor(Processor):
    def converter(self, value: str) -> str:
        conection: dict[str, Any] = {}

        if "-" not in value:
            raise ValueError(f"Missing '-' in conection: {value}")

        word_count = len(value.split())

        if word_count == 1:
            a, b = value.split("-")
            conection["conections"] = tuple((a, b))

        elif word_count == 2:
            left, right = value.split(" ")
            a, b = left.split("-")
            conection["conections"] = tuple((a, b))
            conection["meta_data"] = right

        return conection


class ParserError(Exception):
    pass


class Parser:
    def __init__(self, file_name: str) -> None:
        self.file_name: str = file_name
        self.config = self.get_config()

    def get_config(self) -> dict:
        valid_keys = {"nb_drones": NumericProcessor(),
                  "start_hub": HubProcessor(),
                  "hub": HubProcessor(),
                  "end_hub": HubProcessor(),
                  "connection": ConnectionProcessor()}

        with open(self.file_name, "r") as file:
            config = {}
            ln = 1
            keys_numbers = 2

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

                if key in config.keys():
                    new_key = f"{key}_{keys_numbers}"

                    if key == "connection":
                        keys_numbers = 1

                    keys_numbers += 1
                    config[new_key] = valid_keys[key].converter(value)
                else:
                    config[key] = valid_keys[key].converter(value)

                ln += 1

        flag = __verify_config(config)

        return config

        def __verify_config(self, config: dict[str, Any]) -> list[str]:
            erros: list[str] = []
            if "nb_drones" not in config:
                erros.append("Missing key nb_drones")
            if "nb_drones" and 
