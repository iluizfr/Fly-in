from .Drone import Drone
from typing import Any


class HubError(Exception):
    """
    Represents an error raised while processing hub configuration.

    This exception is used when hub metadata contains an invalid format,
    unknown configuration keys, invalid zone types, or invalid values.
    """
    pass


class Hub:
    """
    Represents a hub in the drone network.

    A hub stores its name, position, configuration metadata, and the drones
    currently occupying it. Its metadata also determines the hub's zone type,
    color, and maximum number of drones it can contain.
    """

    def __init__(self, name: str, pos: tuple[int, int],
                 meta_data: str, line: int) -> None:
        """
        Initializes a hub with its name, position, and optional metadata.

        The metadata is parsed and validated during initialization to determine
        the hub's zone type, color, and maximum drone capacity.
        """
        self.name: str = name
        self.pos: tuple[int, int] = pos
        self.line: int = line
        self.meta_data: dict[str, Any] = self.__check_meta_data(meta_data)
        self.drones: list[Drone] = []
        self.type: str = self.meta_data["zone"]
        self.color: str | None = self.meta_data["color"]
        self.max_drones: int = self.meta_data["max_drones"]

    def __repr__(self) -> str:
        """
        Returns a string representation of the hub.

        The hub is represented by its name.
        """
        return self.name

    def __check_meta_data(self, meta_data: str) -> dict[str, Any]:
        """
        Parses and validates the hub metadata.

        The method extracts supported configuration values such as the hub's
        color, maximum drone capacity, and zone type. Default values are used
        when no metadata is provided.
        """
        keys = ["color", "max_drones", "zone"]
        valid_zones = ["normal", "blocked", "restricted", "priority"]
        new_meta_data: dict[str, Any] = {}

        new_meta_data["zone"] = "normal"
        new_meta_data["color"] = None
        new_meta_data["max_drones"] = 1
        ln = self.line

        if not meta_data or not meta_data.strip():
            return new_meta_data

        if not meta_data.startswith("[") or not meta_data.endswith("]"):
            raise HubError(
                f"line: {ln}, meta data must start and end with '[]'.")

        meta_data = meta_data.strip("[")
        meta_data = meta_data.strip("]")
        datas = meta_data.split()

        for data in datas:
            if "=" not in data:
                raise HubError(
                    f"line: {ln}, wrong format in '{data}', missing '='.")

            key, value = data.split("=")

            if key not in keys:
                raise HubError(
                    f"line: {ln}, wrong key '{key}' in meta data.")

            if key == "max_drones":
                try:
                    new_meta_data[key] = int(value)
                except ValueError:
                    raise HubError(
                        f"line: {ln}, '{value}' not valid for '{key}'.")

                if new_meta_data[key] < 0:
                    raise HubError(
                        f"line: {ln}, no negative values for '{key}'.")

            elif key == "color" or key == "zone":
                if key == "zone" and value not in valid_zones:
                    raise HubError(f"line: {ln}, unknow zone type '{value}'.")

                new_meta_data[key] = value.strip()

        return new_meta_data

    def movement_cost(self) -> int:
        """
        Returns the movement cost associated with this hub.

        Restricted hubs have a higher movement cost, while all other hub types
        use the default movement cost.
        """
        if self.type == "restricted":
            return 2
        return 1

    def is_blocked(self) -> bool:
        """
        Checks whether the hub is blocked.

        Returns True when the hub's zone type is set to "blocked", otherwise
        returns False.
        """
        return self.type == "blocked"

    def has_space(self) -> bool:
        """
        Checks whether the hub has available capacity for another drone.

        Returns True when the current number of drones is below the hub's
        maximum capacity, and False when the hub is full.
        """
        return len(self.drones) < self.max_drones
