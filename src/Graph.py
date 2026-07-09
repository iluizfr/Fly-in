from typing import Any
from .Hub import Hub
from .Connection import Connection
from .Drone import Drone
from .Parser import Parser


class Graph():
    def __init__(self, parser: Parser) -> None:
        self.nb_drones: int = parser.nb_drones
        self.start_hub: Hub = parser.start_hub
        self.hubs: list[Hub] = parser.hubs
        self.connections: list[Connection] = parser.connections
        self.end_hub: Hub = parser.end_hub
        self.drones: list[Drone] = []
        self.dict_graph: dict[Hub, list[Hub]] = self.__set_dict_graph()
        self.__generate_drones()

    def __set_dict_graph(self) -> dict[Hub, list[Hub]]:
        graph: dict[Hub, list[Hub]] = {}
        node_a = None
        node_b = None

        for c in self.connections:
            a, b = c.connection

            if a == self.start_hub.name:
                node_a = self.start_hub
            elif a == self.end_hub.name:
                node_a = self.end_hub
            if b == self.start_hub.name:
                node_b = self.start_hub
            elif b == self.end_hub.name:
                node_b = self.end_hub

            for hub in self.hubs:
                if a == hub.name:
                    node_a = hub
                elif b == hub.name:
                    node_b = hub

            graph.setdefault(node_a, []).append(node_b)

        return graph

    def __generate_drones(self) -> None:
        drone_id = 1

        for i in range(self.nb_drones):
            new_drone_id = f"D{drone_id}"
            drone = Drone(new_drone_id)
            self.drones.append(drone)
            drone_id += 1

    def hubs_info(self) -> None:
        print("start_hub:")
        print(f"    name: {self.start_hub.name}")
        print(f"    pos: {self.start_hub.pos}")
        print(f"    meta data: {self.start_hub.meta_data}\n")

        print("Hubs:")
        for hub in self.hubs:
            print(f"    name: {hub.name}")
            print(f"    pos: {hub.pos}")
            print(f"    meta data: {hub.meta_data}\n")

        print("end_hub:")
        print(f"    name: {self.end_hub.name}")
        print(f"    pos: {self.end_hub.pos}")
        print(f"    meta data: {self.end_hub.meta_data}\n")

    def drones_info(self) -> None:
        print(f"Number of drones: {self.nb_drones}")
        for d in self.drones:
            print(f"{d.id}")

    def dict_graph_info(self) -> None:
        print("Representation of the dict 'graph'..\n")

        for key, value in self.dict_graph.items():
            print(f"{key.name}: ", end="")
            i = 1

            for sub_value in value:
                print(f"{sub_value.name}", end="")

                if i != len(value):
                    print(", ", end="")
                i += 1
            print()
