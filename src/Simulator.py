from .Graph import Graph
from .Drone import Drone
from .Hub import  Hub


class Simulator:
    def __init__(self, graph: Graph) -> None:
        self.class_graph = graph
        self.drones = graph.drones
        self.start_hub = graph.start_hub
        self.end_hub = graph.end_hub
        self.delivered_drones = []
        self.graph: dict[Hub: list[Hub]] = graph.dict_graph
        self.current_turn = 0

        for drone in self.drones:
            drone.current_hub = self.start_hub
            drone.path = self.class_graph.find_path(self.start_hub, self.end_hub)
            graph.start_hub.drones.append(drone)

    def simulate(self):
        while self.drones:
            self.simulate_turn()
            self.current_turn += 1
            print()

    def simulate_turn(self) -> None:
        for drone in self.drones[:]:

            current_hub = drone.current_hub
            drone.path = self.class_graph.find_path(current_hub, self.end_hub)

            if len(drone.path) < 2:
                self.delivered_drones.append(drone)

                if drone in self.end_hub.drones:
                    self.end_hub.drones.remove(drone)

                self.drones.remove(drone)
                continue

            self.move_drone(drone)

            if drone in self.end_hub.drones:
                self.delivered_drones.append(drone)
                self.end_hub.drones.remove(drone)
                self.drones.remove(drone)

    def move_drone(self, drone: Drone) -> None:
        current_hub = drone.path[0]
        next_hub = drone.path[1]

        if next_hub.has_space():
            next_hub.drones.append(drone)
            current_hub.drones.remove(drone)
            drone.current_hub = next_hub

            print(f"{drone.id}-{next_hub.name} ", end="")
