from .Hub import Hub
from .Connection import Connection
from .Drone import Drone
from .Parser import Parser
from collections import deque
import heapq


class Graph():
    def __init__(self, parser: Parser) -> None:
        self.nb_drones: int = parser.nb_drones
        self.start_hub: Hub = parser.start_hub
        self.hubs: list[Hub] = parser.hubs
        self.connections: list[Connection] = parser.connections
        self.end_hub: Hub = parser.end_hub
        self.drones: list[Drone] = []

        self.hub_by_name: dict[str, Hub] = {
            self.start_hub.name: self.start_hub,
            self.end_hub.name: self.end_hub
        }

        for hub in self.hubs:
            self.hub_by_name[hub.name] = hub

        self.dict_graph: dict[Hub, list[Hub]] = self.__set_dict_graph()

        self.__generate_drones()

    def __repr__(self) -> str:
        return "Graph"

    def __set_dict_graph(self) -> dict[Hub, list[Hub]]:
        graph: dict[Hub, list[Hub]] = {}

        for connection in self.connections:
            a, b = connection.connection

            node_a = self.hub_by_name[a]
            node_b = self.hub_by_name[b]

            connection.connection = (node_a, node_b)

            graph.setdefault(node_a, []).append(node_b)
            graph.setdefault(node_b, []).append(node_a)

        return graph

    def __generate_drones(self) -> None:
        drone_id = 1

        for i in range(self.nb_drones):
            new_drone_id = f"D{drone_id}"
            drone = Drone(new_drone_id)
            self.drones.append(drone)
            drone_id += 1

    def bfs(self, start: Hub, end: Hub) -> list[Hub]:
        queue = deque([start])
        visited: set[Hub] = {start}
        father: dict[Hub, Hub] = {}

        while queue:
            current = queue.popleft()

            if current == end:
                break

            for neighbor in self.dict_graph.get(current, []):

                if neighbor.is_blocked():
                    continue

                if neighbor not in visited:
                    visited.add(neighbor)
                    father[neighbor] = current
                    queue.append(neighbor)

        if end not in visited:
            return []

        path = []
        current = end

        while current != start:
            path.append(current)
            current = father[current]

        path.append(start)
        path.reverse()

        return path

    def dijkstra(self, start: Hub, end: Hub) -> list[Hub]:
        distances = {hub: float("inf") for hub in self.dict_graph}
        previous = {hub: None for hub in self.dict_graph}

        distances[start] = 0
        queue = [(0, start.name, start)]

        while queue:
            current_distance, _, current = heapq.heappop(queue)

            if current == end:
                break

            if current_distance > distances[current]:
                continue

            for neighbor in self.dict_graph[current]:
                if neighbor != end and neighbor.is_blocked():
                    continue

                weight = neighbor.movement_cost()
                new_distance = current_distance + weight

                if neighbor.type == "priority":
                    weight -= 1

                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous[neighbor] = current
                    heapq.heappush(
                        queue, (new_distance, neighbor.name, neighbor))

        path = []
        node = end

        while node is not None:
            path.append(node)
            node = previous[node]

        path.reverse()

        if path[0] != start:
            return []

        return path

    def get_connection(self, hub_a: Hub, hub_b: Hub) -> Connection | None:
        for connection in self.connections:
            a, b = connection.connection

            if (a == hub_a and b == hub_b) or (a == hub_b and b == hub_a):
                return connection

        return None

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
