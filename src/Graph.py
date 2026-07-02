from typing import Any
from .Hub import Hub
from .Connection import Connection
from .Drone import Drone


class Graph:
    def __init__(self) -> None:
        self.hubs: list[Hub] = []
        self.connections: list[Connection] = []
        self.drones: list[Drone] = []

    def add_hubs(self, hub: list[Hub]) -> None:
        self.hubs.append(hub)

    def add_connections(self, connections: list[Connection]) -> None:
        self.connections.append(connections)

    def add_drones(self, drones: list[Drone]) -> None:
        self.add_drones.append(drones)

    def info(self) -> None:
        print(f"Number of hubs: {len(self.hubs)}\n")

        print("Hubs:")
        for hub in self.hubs:
            print(f"name: {hub.name}\nposition: {hub.pos}\nmeta datas: {hub.meta_data}\n")
