from typing import Any
from .Hub import Hub


class Graph:
    def __init__(self) -> None:
        self.hubs: list[Hub] = []

    def add_hub(self, hub: Hub) -> None:
        self.hubs.append(hub)

    def info(self) -> None:
        print(f"Number of hubs: {len(self.hubs)}\n")
        print("Hubs:")

        for hub in self.hubs:
            print(f"name: {hub.name}\nposition: {hub.pos}\nmeta datas: {hub.meta_data}\n")
