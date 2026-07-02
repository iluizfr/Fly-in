from typing import Any
from .Drone import Drone
from .Connection import Connection


class HubError(Exception):
    pass


class Hub:
    def __init__(self, name: str, pos: tuple, meta_data: str) -> None:
        self.name: str = name
        self.pos: tuple[int, int] = pos
        self.meta_data: dict[str, Any] = self.__check_meta_data(meta_data)
        self.drones: list[Drone] = []
        self.connection: Connection = None

    def __check_meta_data(self, meta_data: str) -> dict:
        keys = ["color", "max_drones", "zone", "max_link_capacity"]
        valid_zones = ["normal", "blocked", "restricted", "priority"]
        new_meta_data: dict[str, Any] = {}

        if not meta_data or not meta_data.strip():
            return {}

        meta_data = meta_data.strip("[")
        meta_data = meta_data.strip("]")
        datas = meta_data.split()

        for data in datas:
            if "=" not in data:
                raise HubError(f"Hub: wrong format in meta data: {data}")
            key, value = data.split("=")

            if key not in keys:
                raise HubError(f"Hub: Wrong key in {meta_data}")

            if key == "max_drones" or key == "max_link_capacity":
                new_meta_data[key] = int(value)

                if new_meta_data[key] < 0:
                    raise HubError(f"Values for '{key}' must be positive")

            elif key == "color" or key == "zone":
                if key == "zone" and value not in valid_zones:
                    raise HubError(f"Unknow zone type: {value}")

                new_meta_data[key] = value.strip()

        return new_meta_data
