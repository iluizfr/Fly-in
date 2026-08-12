from .Simulator import Simulator
import pygame
import webcolors
from .Hub import Hub


class Renderer:
    def __init__(self, simulator: Simulator) -> None:
        self.simulator = simulator
        self.scale = 100
        self.hub_size = 20
        self.drone_size = 8

        pygame.init()
        self.screen = pygame.display.set_mode((1000, 700))
        pygame.display.set_caption("Fly-in")

        self.running = True

    def draw(self) -> None:
        self.screen.fill((30, 30, 30))

        font = pygame.font.Font(None, 22)

        # Draw the lines between the hubs
        for connection in self.simulator.class_graph.connections:
            hub_a, hub_b = connection.connection

            x1, y1 = self.pos(hub_a)
            x2, y2 = self.pos(hub_b)

            pygame.draw.line(
                self.screen,
                (255, 255, 255),
                (x1, y1), (x2, y2),
                4
                )

            for drone in connection.drones:

                x = x1 - x2
                y = y1 - y2

                pygame.draw.circle(self.screen,
                                   (255, 0, 0), (x, y),
                                   self.drone_size
                                   )

                text = font.render(drone.id, True, self.collor("black"))
                text_rec = text.get_rect(center=(x, y))
                self.screen.blit(text, text_rec)

        # Draw the Hubs
        for hub in self.simulator.class_graph.hub_by_name.values():
            x, y = self.pos(hub)

            if hub.color is not None:
                color = self.collor(hub.color)
            else:
                color = self.collor("blue")

            pygame.draw.circle(self.screen, color, (x, y), self.hub_size)

        # Draw the Drones and writes the drone id
        for drone in self.simulator.drones:
            if drone.current_hub is None:
                continue

            x, y = self.pos(drone.current_hub)

            pygame.draw.circle(self.screen,
                               (255, 0, 0), (x, y),
                               self.drone_size
                               )

            text = font.render(drone.id, True, self.collor("black"))
            text_rec = text.get_rect(center=(x, y))
            self.screen.blit(text, text_rec)

        pygame.display.flip()

    def update(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    @staticmethod
    def collor(collor: str) -> tuple[int, int, int]:
        collor = collor.lower()

        if collor == "rainbow":
            return (23, 34, 98)

        cor = webcolors.name_to_rgb(collor)
        rgb = (cor.red, cor.green, cor.blue)

        return rgb

    def pos(self, hub: Hub) -> tuple[int, int]:
        scale = self.scale

        min_x = min(
            h.pos[0] for h in self.simulator.class_graph.hub_by_name.values())
        max_x = max(
            h.pos[0] for h in self.simulator.class_graph.hub_by_name.values())

        min_y = min(
            h.pos[1] for h in self.simulator.class_graph.hub_by_name.values())
        max_y = max(
            h.pos[1] for h in self.simulator.class_graph.hub_by_name.values())

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
