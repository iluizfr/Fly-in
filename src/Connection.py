from typing import Optional, Any
from .Drone import Drone


class ConectionError(Exception):
    """
    Represents an error raised while processing connection configuration.

    This exception is used when a connection contains invalid metadata,
    unknown configuration keys, or invalid values.
    """
    pass


class Connection:
    """
    Represents a connection between two hubs.

    A connection can contain metadata such as its maximum capacity and keeps
    track of the drones currently using it. It provides methods to check
    available space and to manage drones entering or leaving the connection.
    """

    def __init__(self, connection: tuple[Any, Any], line: int,
                 meta_data: Optional[str] = None) -> None:
        """
        Initializes a connection between two hubs.

        The connection stores the names or identifiers of both hubs and
        processes the optional metadata to determine the connection's
        maximum drone capacity.
        """
        self.connection: tuple[Any, Any] = connection
        self.line = line
        self.meta_data: dict[str, Any] = self.__check_meta_data(meta_data)
        self.max_capacity = self.meta_data["max_link_capacity"]
        self.drones: list[Drone] = []

    def __repr__(self) -> str:
        """
        Returns a string representation of the connection.

        The representation includes the two hubs connected by this
        connection.
        """
        a, b = self.connection
        return f"Connection: {a}, {b}"

    def has_space(self) -> bool:
        """
        Checks whether the connection has available capacity.

        Returns True when the number of drones currently using the connection
        is below its maximum capacity, and False otherwise.
        """
        has_space = len(self.drones) < self.max_capacity

        return bool(has_space)

    def __check_meta_data(self, meta_data: str | None) -> dict[str, Any]:
        """
        Parses and validates the connection metadata.

        The method extracts supported configuration values from the metadata
        and sets the maximum link capacity. If no metadata is provided, the
        connection uses a default capacity of one drone.
        """
        keys = ["max_link_capacity"]
        new_meta_data: dict[str, Any] = {}

        new_meta_data["max_link_capacity"] = 1
        ln = self.line

        if not meta_data or not meta_data.strip():
            return new_meta_data

        if not meta_data.startswith("[") or not meta_data.endswith("]"):
            raise ConectionError(
                f"line: {ln}, meta data must start and end with '[]'.")

        meta_data = meta_data.strip("[")
        meta_data = meta_data.strip("]")

        datas = meta_data.split()

        for data in datas:
            key, value = data.split("=")

            if key not in keys:
                raise ConectionError(
                    f"line: {ln}, unknow key in {meta_data}.")

            if key == "max_link_capacity":
                new_meta_data[key] = int(value)
                if new_meta_data[key] < 0:
                    raise ConectionError(
                        f"line: {ln}, values for '{key}' must be positive'")

        return new_meta_data

    def enter(self, drone: Drone) -> bool:
        """
        Adds a drone to the connection if capacity is available.

        Returns False when the connection has reached its maximum capacity.
        Otherwise, the drone is added to the connection and the method
        returns True.
        """
        if not self.has_space():
            return False

        self.drones.append(drone)
        return True

    def leave(self, drone: Drone) -> None:
        """
        Removes a drone from the connection.

        If the drone is currently using the connection, it is removed.
        Otherwise, the connection remains unchanged.
        """
        if drone in self.drones:
            self.drones.remove(drone)
