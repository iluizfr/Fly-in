from .Simulator import Simulator
import pygame


class Renderer:
    def __init__(self, simulator: Simulator):
        self.simulator = simulator
        self.scale = 100
        self.hub_size = 20
        self.drone_size = 8

        pygame.init()
        self.screen = pygame.display.set_mode((1000, 700))
        pygame.display.set_caption("Fly-in")

        self.running = True

    def draw(self):
        self.screen.fill((30, 30, 30))

        font = pygame.font.SysFont(None, 22)

        for connection in self.simulator.class_graph.connections:
            hub_a, hub_b = connection.connection

            x1, y1 = self.pos(hub_a)
            x2, y2 = self.pos(hub_b)

            pygame.draw.line(self.screen, (255, 255, 255), (x1, y1), (x2, y2), 4)


        for hub in self.simulator.class_graph.hub_by_name.values():
            x, y = self.pos(hub)

            if hub.color is not None:
                color = self.collor(hub.color)
            else:
                color = self.collor("blue")

            pygame.draw.circle(self.screen, color, (x, y), self.hub_size)


        for drone in self.simulator.drones:
            if drone.current_hub is None:
                continue

            x, y = self.pos(drone.current_hub)

            pygame.draw.circle(self.screen, (255, 0, 0), (x, y), self.drone_size)

        x, y = self.pos(self.simulator.end_hub)
        y -= 40
        x -= 40

        for drone in self.simulator.delivered_drones:
            x += 20

            pygame.draw.circle(self.screen, (255, 0, 0), (x, y), self.drone_size)

        pygame.display.flip()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    @staticmethod
    def collor(collor: str) -> tuple[int, int, int]:
        collors = {
            "green": (0, 255, 00),
            "red": (255, 0, 0),
            "blue": (0, 0, 255),
            "black": (0, 0, 0),
            "white": (255, 255, 255),
            "yellow": (255, 255, 0),
            "orange": (250, 165, 0),
            "gray": (128, 128, 128),
            "brown": (139, 69, 19),
            "pink": (255, 192, 203),
            "cyan": (0, 255, 255),
            "purple": (128, 0, 128),
            "gold": (255, 215, 0),
            "lime": (50, 205, 50),
            "magenta": (255, 0, 255)
        }

        collor = collor.lower()

        if collor not in collors:
            return collors["white"]

        return collors[collor]

    def pos(self, hub: Hub) -> tuple[int, int]:
        scale = self.scale

        min_x = min(h.pos[0] for h in self.simulator.class_graph.hub_by_name.values())
        max_x = max(h.pos[0] for h in self.simulator.class_graph.hub_by_name.values())

        min_y = min(h.pos[1] for h in self.simulator.class_graph.hub_by_name.values())
        max_y = max(h.pos[1] for h in self.simulator.class_graph.hub_by_name.values())

        width = (max_x - min_x) * scale
        height = (max_y - min_y) * scale

        off_x = (self.screen.get_width() - width) // 2
        off_y = (self.screen.get_height() - height) // 2

        x = (hub.pos[0] - min_x) * scale + off_x
        y = (hub.pos[1] - min_y) * scale + off_y

        return x, y

    def set_sizes(self, scale: int, hub_size: int, drone_size: int) -> None:
        self.scale = scale
        self.hub_size = hub_size
        self.drone_size = drone_size