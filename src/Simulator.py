from src.Connection import Connection
from .Graph import Graph
from .Drone import Drone
from .Hub import Hub


class Simulator:
    def __init__(self, graph: Graph) -> None:
        self.class_graph: Graph = graph
        self.drones: list[Drone] = graph.drones
        self.start_hub: Hub = graph.start_hub
        self.end_hub: Hub = graph.end_hub
        self.delivered_drones: list[Drone] = []
        self.graph: dict[Hub, list[Hub]] = graph.dict_graph
        self.current_turn = 0

        for drone in self.drones:
            drone.current_hub = self.start_hub
            drone.current_connection = None
            drone.destination_hub = None
            drone.just_arrived = False
            drone.path = self.class_graph.dijkstra(self.start_hub, self.end_hub)
            self.start_hub.drones.append(drone)

    def __repr__(self) -> str:
        return "Simulator"

    def simulate_turn(self) -> bool:
        printed = False

        for drone in self.drones:
            if drone.remaining_turns > 0:
                drone.remaining_turns -= 1

        for drone in self.drones:
            if (
                drone.current_connection is not None
                and drone.remaining_turns == 0
                ):
                self.finish_restricted_move(drone)
                drone.just_arrived = True

        for drone in self.drones[:]:
            if drone.remaining_turns > 0:
                continue

            if drone.just_arrived:
                drone.just_arrived = False
                continue

            current_hub = drone.current_hub
            drone.path = self.class_graph.dijkstra(current_hub, self.end_hub)

            if len(drone.path) < 2 and drone.path is not None:
                self.delivered_drones.append(drone)

                if drone in self.end_hub.drones:
                    self.end_hub.drones.remove(drone)

                self.drones.remove(drone)
                continue

            if self.move_drone(drone):
                printed = True

            #if drone in self.end_hub.drones:
                #self.delivered_drones.append(drone)
                #self.end_hub.drones.remove(drone)
                #self.drones.remove(drone)

        return printed

    def move_drone(self, drone: Drone) -> bool:
        current_hub = drone.path[0]
        next_hub = drone.path[1]

        connection = self.get_next_connection(current_hub, next_hub)

        if connection is None:
            return False

        if next_hub.type != "restricted":
            if not next_hub.has_space():
                return False

        if not connection.enter(drone):
            return False

        if next_hub.type == "restricted":
            return self.start_restricted_move(drone, current_hub,
                                              next_hub, connection)

        return self.normal_move(drone, current_hub, next_hub, connection)

    def get_next_connection(self, current_hub: Hub, next_hub: Hub):
        return self.class_graph.get_connection(current_hub, next_hub)

    def normal_move(self, drone: Drone, current_hub: Hub,
                    next_hub: Hub, connection: Connection) -> bool:

        current_hub.drones.remove(drone)
        connection.leave(drone)
        next_hub.drones.append(drone)

        drone.current_hub = next_hub

        print(f"{drone.id}-{next_hub.name}", end=" ")
        return True

    def start_restricted_move(self, drone: Drone, current_hub: Hub,
                              next_hub: Hub, connection: Connection) -> bool:

        current_hub.drones.remove(drone)

        drone.current_hub = None
        drone.current_connection = connection
        drone.destination_hub = next_hub
        drone.remaining_turns = 1

        print(f"{drone.id}-{current_hub.name}-{next_hub.name}", end=" ")
        return True

    def finish_restricted_move(self, drone: Drone) -> None:
        connection = drone.current_connection

        connection.leave(drone)

        destination = drone.destination_hub

        destination.drones.append(drone)

        drone.current_hub = destination
        drone.current_connection = None
        drone.destination_hub = None
        drone.remaining_turns = 0
