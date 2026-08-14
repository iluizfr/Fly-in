from src.Connection import Connection
from .Drone import Drone
from .Graph import Graph
from .Hub import Hub


class Simulator:
    """
    Manages the drone simulation and its movement through the graph.

    The simulator controls the state of all drones, determines their routes,
    processes each simulation turn, and handles movement through normal and
    restricted hubs until the drones reach their destination.
    """

    def __init__(self, graph: Graph) -> None:
        """
        Initializes the simulator using the provided graph.

        Each drone is placed at the starting hub and receives an initial path
        to the destination. The simulator also initializes the state required
        to track drone movements and completed deliveries.
        """
        self.class_graph: Graph = graph
        self.drones: list[Drone] = graph.drones
        self.start_hub: Hub | None = graph.start_hub
        self.end_hub: Hub | None = graph.end_hub
        self.delivered_drones: list[Drone] = []
        self.graph: dict[Hub, list[Hub]] = graph.dict_graph
        self.current_turn = 0

        # initialize drones values and give a start path for all
        for drone in self.drones:
            drone.current_hub = self.start_hub
            drone.current_connection = None
            drone.destination_hub = None
            drone.just_arrived = False
            drone.path = self.class_graph.dijkstra(
                self.start_hub, self.end_hub)
            if self.start_hub is not None:
                self.start_hub.drones.append(drone)

    def __repr__(self) -> str:
        """
        Returns a string representation of the simulator.
        """
        return "Simulator"

    def simulate_turn(self) -> None:
        """
        Processes one turn of the drone simulation.

        The method updates the remaining movement time of drones, completes
        restricted movements, recalculates routes, and attempts to move each
        active drone toward its destination. Drones that reach the destination
        are removed from the active simulation and stored as delivered drones.
        """
        printed = False

        for drone in self.drones:
            if drone.remaining_turns > 0:
                drone.remaining_turns -= 1

        for drone in self.drones:
            if (
                drone.current_connection is not None
                    and drone.remaining_turns == 0):

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

                if self.end_hub is not None and drone in self.end_hub.drones:
                    self.end_hub.drones.remove(drone)

                self.drones.remove(drone)
                continue

            if self.move_drone(drone):
                printed = True

        self.current_turn += 1

        if printed:
            print()

    def move_drone(self, drone: Drone) -> bool:
        """
        Attempts to move a drone to the next hub in its current path.

        The method checks whether the next connection exists and whether the
        destination hub and connection have available capacity. Restricted
        hubs are handled separately because entering them requires multiple
        turns to complete the movement.
        """
        current_hub: Hub = drone.path[0]
        next_hub: Hub = drone.path[1]

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

    def get_next_connection(self, current_hub: Hub,
                            next_hub: Hub) -> Connection | None:
        """
        Finds the connection between the current and next hub.

        Delegates the search to the graph and returns the corresponding
        connection if the two hubs are directly connected.
        """
        return self.class_graph.get_connection(current_hub, next_hub)

    def normal_move(self, drone: Drone, current_hub: Hub,
                    next_hub: Hub, connection: Connection) -> bool:
        """
        Moves a drone directly from one hub to another.

        The drone is removed from its current hub and connection, then added
        to the destination hub. Its current location is updated and the
        movement is displayed in the simulation output.
        """
        current_hub.drones.remove(drone)
        connection.leave(drone)
        next_hub.drones.append(drone)

        drone.current_hub = next_hub

        grn = "\033[32m"
        en = "\033[0m"

        print(f"{grn}{drone.id}-{next_hub.name}{en}", end=" ")
        return True

    def start_restricted_move(self, drone: Drone, current_hub: Hub,
                              next_hub: Hub, connection: Connection) -> bool:
        """
        Starts a multi-turn movement through a restricted hub.

        The drone leaves its current hub and remains associated with the
        connection while the movement is in progress. Its destination and
        remaining movement time are stored so the movement can be completed
        on a subsequent turn.
        """
        current_hub.drones.remove(drone)

        drone.current_hub = None
        drone.current_connection = connection
        drone.destination_hub = next_hub
        drone.remaining_turns = 1

        bky = "\033[33m"
        en = "\033[0m"

        print(
            f"{bky}{drone.id}-{current_hub.name}-{next_hub.name}{en}", end=" ")
        return True

    def finish_restricted_move(self, drone: Drone) -> None:
        """
        Completes a drone's movement through a restricted hub.

        The drone is removed from the connection and added to its destination
        hub. Its temporary movement state is then cleared so it can continue
        along its route on the next simulation turn.
        """
        connection = drone.current_connection

        if connection is not None:
            connection.leave(drone)

        destination = drone.destination_hub

        if destination is not None:
            destination.drones.append(drone)

        drone.current_hub = destination
        drone.current_connection = None
        drone.destination_hub = None
        drone.remaining_turns = 0
