from typing import Any
from .Hub import Hub
from .Connection import Connection


class Graph:
    def __init__(self) -> None:
        self.hubs: list[Hub] = []
        self.connections[Connection] = []

    def add_hub(self, hub: list[Hub]) -> None:
        self.hubs.append(hub)

    def info(self) -> None:
        print(f"Number of hubs: {len(self.hubs)}\n")
        print("Hubs:")

        for hub in self.hubs:
            print(f"name: {hub.name}\nposition: {hub.pos}\nmeta datas: {hub.meta_data}\n")
