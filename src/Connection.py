from typing import Optional, Any
from .Drone import Drone


class ConectionError(Exception):
    pass


class Connection:
    def __init__(self, connection: tuple[Any, Any],
                 meta_data: Optional[str] = None) -> None:

        self.connection: tuple[Any, Any] = connection
        self.meta_data: dict[str, Any] = self.__check_meta_data(meta_data)
        self.max_capacity = self.meta_data["max_link_capacity"]
        self.drones: list[Drone] = []

    def __repr__(self) -> str:
        a, b = self.connection
        return f"Connection: {a}, {b}"

    def has_space(self) -> bool:
        has_space = len(self.drones) < self.max_capacity

        return bool(has_space)

    def __check_meta_data(self, meta_data: str | None) -> dict[str, Any]:
        keys = ["max_link_capacity"]
        new_meta_data: dict[str, Any] = {}

        new_meta_data["max_link_capacity"] = 1

        if not meta_data or not meta_data.strip():
            return new_meta_data

        meta_data = meta_data.strip("[")
        meta_data = meta_data.strip("]")

        datas = meta_data.split()

        for data in datas:
            key, value = data.split("=")

            if key not in keys:
                raise ConectionError(f"Connection: Unknow key in {meta_data}")

            if key == "max_link_capacity":
                new_meta_data[key] = int(value)
                if new_meta_data[key] < 0:
                    raise ConectionError(
                        f"Values for '{key}' must be positive'")

        return new_meta_data

    def enter(self, drone: Drone) -> bool:
        if not self.has_space():
            return False

        self.drones.append(drone)
        return True

    def leave(self, drone: Drone) -> None:
        if drone in self.drones:
            self.drones.remove(drone)
