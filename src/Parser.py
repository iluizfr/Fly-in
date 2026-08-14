from abc import ABC, abstractmethod
from .Connection import Connection
from typing import Any
from .Hub import Hub


class Processor(ABC):
    """
    Base class for processors responsible for converting configuration values.

    Subclasses must implement the converter method to transform a string value
    into the appropriate data type or structure.
    """

    @abstractmethod
    def converter(self, value: str) -> Any:
        """
        Converts a string value into the expected data type or structure.
        """
        pass


class NumericProcessor(Processor):
    """
    Processes numeric configuration values.

    This processor converts string values into positive integers and raises
    an error when the resulting value is not greater than zero.
    """

    def converter(self, value: str) -> int:
        """
        Converts a string value into a positive integer.

        The value is validated before being returned.
        """
        return self.validate(value)

    @staticmethod
    def validate(value: str) -> int:
        """
        Validates and converts a string value into a positive integer.

        Raises an error if the value cannot be converted to an integer or
        if the resulting number is less than or equal to zero.
        """
        new_value = int(value)
        if new_value <= 0:
            raise ValueError("Parsing: nb_drones must be bigger than 0")
        return new_value


class HubProcessor(Processor):
    """
    Processes hub configuration values.

    This processor parses a hub definition and extracts its name, coordinates,
    and optional metadata into a dictionary.
    """

    def converter(self, value: str) -> Any:
        """
        Parses a hub configuration string into a dictionary.

        The resulting dictionary contains the hub name, its coordinates,
        and any additional metadata provided in the configuration.
        """
        hub: dict[str, Any] = {}
        pre_check: list[str] = value.split()

        try:
            n = int(pre_check[1])
            n = n
        except Exception:
            raise ParserError(
                "Hubprocessor: ' ' not allowed in names of hub's")

        name = pre_check[0]
        x = pre_check[1]
        y = pre_check[2]
        meta_data: str = ""
        meta_data += " ".join(pre_check[3:])

        if "-" in name:
            raise ValueError(
                "HubProcessor: '-' not allowed in names of hub's")
        hub["name"] = name
        hub["coordinate"] = tuple((int(x), int(y)))
        hub["meta_data"] = meta_data

        return hub


class ConnectionProcessor(Processor):
    """
    Processes connection configuration values.

    This processor parses a connection definition and extracts the names of
    the connected hubs along with any optional metadata.
    """

    def converter(self, value: str) -> dict[str, Any]:
        """
        Parses a connection configuration string into a dictionary.

        The connection is represented by the names of the two connected hubs.
        Optional metadata is also included when provided.
        """
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
    """
    Represents an error raised while parsing or validating the configuration.

    This exception is used when the configuration file contains invalid
    syntax, duplicated values, missing values, or invalid connections.
    """
    pass


class Parser:
    """
    Parses and validates a configuration file.

    The parser reads the configuration file, processes each supported entry,
    and creates the corresponding hubs and connections. It also validates
    the configuration to ensure that required values are present and that
    hubs and connections do not contain invalid or duplicated data.
    """

    def __init__(self, file_name: str) -> None:
        """
        Initializes the parser with the path of the configuration file.

        The configuration is automatically parsed and validated during
        initialization.
        """
        self.connections: list[Connection] = []
        self.file_name: str = file_name
        self.start_hub: Hub | None = None
        self.hubs: list[Hub] = []
        self.nb_drones: int = 0
        self.end_hub: Hub | None = None
        self.ln = 1
        self.set_config()

    def __repr__(self) -> str:
        """
        Returns a string representation of the parser instance.
        """
        return "Parser"

    def set_config(self) -> None:
        """
        Reads and processes the configuration file.

        Each valid configuration entry is parsed using its corresponding
        processor. The method creates the configured hubs and connections,
        validates required entries, and performs a final connection check.
        """
        stack_keys: list[str] = []
        stack_names: list[str] = []
        stack_coordinate: list[tuple[int, int]] = []
        valid_keys: dict[str, Any] = {"nb_drones": NumericProcessor(),
                                      "start_hub": HubProcessor(),
                                      "hub": HubProcessor(),
                                      "end_hub": HubProcessor(),
                                      "connection": ConnectionProcessor()}

        with open(self.file_name, "r") as file:
            empty = file

            # Check if the file is empty
            if not empty.read().strip():
                raise ParserError(f"Parser: Empty file '{self.file_name}'")

            # Comeback for the beginning of the line
            file.seek(0)

            for line in file:
                line = line.strip()

                # Skip empty lines and comentaries
                if not line or line.startswith("#"):
                    self.ln += 1
                    continue

                # Valid lines have ":"
                elif ":" not in line:
                    raise ParserError(
                        f"Syntax: {self.file_name} line {self.ln} missing ':'")

                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()

                # Check if the key is valid
                if key not in valid_keys.keys():
                    raise ParserError(
                        f"Parser: Unknown key in '{key}' in line {self.ln}")

                # Check repeated key
                if key in stack_keys:
                    if key == "hub" or key == "connection":
                        pass
                    else:
                        raise ParserError(
                            f"Duplicated key: '{key}' in line: {self.ln}")

                stack_keys.append(key)

                # Number of Drones
                if key == "nb_drones":
                    if self.start_hub is not None or len(self.hubs) != 0 \
                        or self.end_hub is not None \
                            or len(self.connections) != 0:
                        raise ParserError(
                            "Parser: nb_drones not in first valid line")
                    config = valid_keys[key].converter(value)
                    self.nb_drones = config

                # Start Hub
                elif key == "start_hub":
                    if self.start_hub is not None:
                        raise ParserError(
                            f"Duplicate start_hub in line {self.ln}")
                    else:
                        config = valid_keys[key].converter(value)

                        if config["name"] in stack_names:
                            raise ParserError(
                                f"Duplicated start_hub name in line {self.ln}")

                        if config["coordinate"] in stack_coordinate:
                            raise ParserError(
                                f"Duplicated coordinate in line {self.ln}"
                            )

                        self.start_hub = Hub(
                            config["name"],
                            config["coordinate"],
                            config["meta_data"]
                            )
                        stack_names.append(config["name"])
                        stack_coordinate.append(config["coordinate"])

                # Hub
                elif key == "hub":
                    config = valid_keys[key].converter(value)

                    if config["name"] in stack_names:
                        raise ParserError(
                            f"Duplicated hub name in line {self.ln}")

                    if config["coordinate"] in stack_coordinate:
                        raise ParserError(
                            f"Duplicated coordinate in line {self.ln}"
                        )

                    self.hubs.append(Hub(config["name"],
                                         config["coordinate"],
                                         config["meta_data"]))

                    stack_names.append(config["name"])
                    stack_coordinate.append(config["coordinate"])

                # End Hub
                elif key == "end_hub":
                    if self.end_hub is not None:
                        raise ParserError(
                            f"Duplicate end_hub in line {self.ln}")
                    else:
                        config = valid_keys[key].converter(value)

                        if config["name"] in stack_names:
                            raise ParserError(
                                f"Duplicated end_hub name in line {self.ln}")

                        if config["coordinate"] in stack_coordinate:
                            raise ParserError(
                                f"Duplicated coordinate in line {self.ln}"
                            )

                        self.end_hub = Hub(config["name"],
                                           config["coordinate"],
                                           config["meta_data"])
                        stack_names.append(config["name"])
                        stack_coordinate.append(config["coordinate"])

                # Connection
                elif key == "connection":
                    config = valid_keys[key].converter(value)

                    if "meta_data" in config:
                        self.connections.append(
                            Connection(config["connections"],
                                       config["meta_data"]))
                    else:
                        self.connections.append(
                            Connection(config["connections"]))

                self.ln += 1

        for key in valid_keys.keys():
            if key not in stack_keys:
                raise ParserError(f"Parser: Missing key '{key}'")

        # Extra security
        self.__check_connections()

    def __check_connections(self) -> None:
        """
        Validates all connections defined in the configuration.

        Checks that connections reference existing hubs, do not connect a hub
        to itself, and are not duplicated or defined in reverse order.
        """
        previus_connections = []
        previus_reverse_connections = []
        hubs_names: list[str] = []

        hubs_names = [hub.name for hub in self.hubs]

        if self.start_hub is not None and self.end_hub is not None:
            hubs_names.append(self.start_hub.name)
            hubs_names.append(self.end_hub.name)

        for c in self.connections:
            a, b = c.connection

            if a == b:
                raise ParserError(f"Connection: Wrong connection '{a}-{b}'")

            if a not in hubs_names:
                raise ParserError(f"Connection: {a} not in hubs names")
            if b not in hubs_names:
                raise ParserError(f"Connection: {b} not in hubs names")

            if c.connection in previus_connections \
                    or c.connection in previus_reverse_connections:
                raise ParserError(f"Duplicated connection: {c.connection}")

            previus_connections.append(tuple((a, b)))
            previus_reverse_connections.append(tuple((b, a)))
