from typing import Optional, Any


class ConectionError(Exception):
    pass


class Connection:
    def __init__(self, connection: tuple[str, str], meta_data: Optional[str] = None) -> None:
        self.connection: tuple[str, str] = connection
        self.meta_data: dict[str, Any] = self.__check_meta_data(meta_data)
        self.max_capacity = self.meta_data["max_link_capacity"]
        self.drones = []

    def __check_meta_data(self, meta_data: str) -> dict:
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
                    raise ConectionError(f"Values for '{key}' must be positive'")

        return new_meta_data

    def has_space(self) -> bool:
        return len(self.drones) < self.max_capacity
