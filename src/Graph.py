from .Connection import Connection
from collections import deque
from .Parser import Parser
from .Drone import Drone
from typing import Any
from .Hub import Hub
import heapq


class Graph():
    """
    Represents the network of hubs and connections used by the simulation.

    The graph stores all hubs, connections, and drones and provides methods
    for finding routes between hubs. It also initializes the network from
    the parsed configuration and validates that a path exists between the
    starting and ending hubs.
    """

    def __init__(self, parser: Parser) -> None:
        """
        Initializes the graph using the configuration provided by the parser.

        The graph builds a lookup table for hubs, creates the graph structure
        from the available connections, checks that the destination is
        reachable from the starting hub, and generates all required drones.
        """
        self.nb_drones: int = parser.nb_drones
        self.start_hub: Hub | None = parser.start_hub
        self.hubs: list[Hub] = parser.hubs
        self.connections: list[Connection] = parser.connections
        self.end_hub: Hub | None = parser.end_hub
        self.drones: list[Drone] = []
        self.hub_by_name: dict[str, Hub] = {}

        # hub_by_name basically a dict to get a hub object by its name
        if self.start_hub is not None and self.end_hub is not None:
            self.hub_by_name = {
                self.start_hub.name: self.start_hub,
                self.end_hub.name: self.end_hub
            }

        for hub in self.hubs:
            self.hub_by_name[hub.name] = hub

        self.dict_graph: dict[Hub, list[Hub]] = self.__set_dict_graph()

        # Check if has a valid way from start to the end
        self.is_valid: bool = True if len(self.bfs(
            self.start_hub, self.end_hub)) != 0 else False

        if not self.is_valid:
            file = parser.file_name
            raise ValueError(
                f"{file} not valid. Drones can't find a way to the end")

        # initialize drones
        self.__generate_drones()

    def __repr__(self) -> str:
        """
        Returns a string representation of the graph.
        """
        return "Graph"

    def __set_dict_graph(self) -> dict[Hub, list[Hub]]:
        """
        Builds the graph structure from the available connections.

        Each connection is converted from hub names to actual Hub objects.
        The resulting dictionary stores each hub and the list of hubs directly
        connected to it, allowing the graph to be traversed efficiently.
        """
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
        """
        Creates the drones required by the configuration.

        Each drone receives a unique identifier and is added to the graph's
        list of active drones.
        """
        drone_id = 1

        for i in range(self.nb_drones):
            new_drone_id = f"D{drone_id}"
            drone = Drone(new_drone_id)
            self.drones.append(drone)
            drone_id += 1

    def bfs(self, start: Any, end: Any) -> list[Hub]:
        """
        Finds a path between two hubs using breadth-first search.

        Blocked hubs are ignored during the search. If a path exists, the
        method returns the sequence of hubs from the starting hub to the
        destination. An empty list is returned when no path can be found.
        """
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

    def dijkstra(self, start: Hub | None, end: Hub | None) -> list[Hub]:
        """
        Finds the lowest-cost path between two hubs using Dijkstra's algorithm.

        The path is calculated using the movement cost of each hub while
        avoiding blocked hubs. Priority hubs receive a reduced movement cost.
        An empty list is returned when the destination cannot be reached.
        """
        distances = {hub: float("inf") for hub in self.dict_graph}
        previous: dict[Hub | None, Hub | None] = {}
        previous = {hub: None for hub in self.dict_graph}

        if start is not None:
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
        """
        Finds the connection between two hubs.

        The search considers both directions because connections are treated
        as bidirectional. Returns the corresponding Connection object when
        one exists, or None when the hubs are not directly connected.
        """
        for connection in self.connections:
            a, b = connection.connection

            if (a == hub_a and b == hub_b) or (a == hub_b and b == hub_a):
                return connection

        return None

    def drones_info(self) -> None:
        """
        Prints information about the drones in the graph.

        Displays the total number of drones followed by the identifier of
        each drone.
        """
        print(f"Number of drones: {self.nb_drones}")
        for d in self.drones:
            print(f"{d.id}")

    def dict_graph_info(self) -> None:
        """
        Prints the graph structure and its connected hubs.

        Each hub is displayed together with the names of all hubs directly
        connected to it.
        """
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
