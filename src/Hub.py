from typing import Any


class Hub:
    def __init__(self, name: str, pos: tuple, meta_data: str) -> None:
        self.name: str = name
        self.pos: tuple[int, int] = pos
        self.meta_data: dict[str, Any] = self.__check_meta_data(meta_data)

    def __check_meta_data(self, meta_data: str) -> dict:
        keys = ["color", "max_drones", "zone", "max_link_capacity"]
        new_meta_data: dict[str, Any] = {}

        if not meta_data or not meta_data.strip():
            return {}

        meta_data = meta_data.strip("[")
        meta_data = meta_data.strip("]")

        datas = meta_data.split()

        for data in datas:
            key, value = data.split("=")

            if key not in keys:
                raise ValueError(f"Wrong key in {meta_data}")

            if key == "max_drones" or key == "max_link_capacity":
                new_meta_data[key] = int(value)
            elif key == "color" or key == "zone":
                new_meta_data[key] = value.strip()

        return new_meta_data
