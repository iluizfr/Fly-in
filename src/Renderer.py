from .Simulator import Simulator
from .Hub import Hub
import webcolors
import pygame


class Renderer:
    """
    Handles the graphical representation of the drone simulation.

    The renderer uses Pygame to display hubs, connections, and drones on the
    screen. It also manages the visual scale and sizes of the elements based
    on the current simulation configuration.
    """

    def __init__(self, simulator: Simulator) -> None:
        """
        Initializes the renderer with the given simulation.

        The Pygame window is created and configured with the default display
        settings. The renderer also starts in a running state, allowing the
        application to process events and update the display.
        """
        self.simulator = simulator
        self.scale = 100
        self.hub_size = 20
        self.drone_size = 8

        pygame.init()
        self.screen = pygame.display.set_mode((1000, 700))
        pygame.display.set_caption("Fly-in")
        self.running = True

    def draw(self) -> None:
        """
        Draws the current state of the simulation on the screen.

        The method renders the connections between hubs, the hubs themselves,
        and all drones that are currently located at a hub. The display is
        refreshed after all elements have been drawn.
        """
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

            # Draw drones in connections
            for drone in connection.drones:
                x = x1 + (x2 - x1) // 2
                y = y1 + (y2 - y1) // 2

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
        """
        Processes Pygame events and updates the renderer state.

        The renderer stops running when a window close event is received.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    @staticmethod
    def collor(collor: str) -> tuple[int, int, int]:
        """
        Converts a color name into an RGB color tuple.

        The color name is normalized to lowercase before being converted.
        The special "rainbow" value uses a predefined RGB color.
        """
        collor = collor.lower()

        if collor == "rainbow":
            return (23, 34, 98)

        cor = webcolors.name_to_rgb(collor)
        rgb = (cor.red, cor.green, cor.blue)

        return rgb

    def pos(self, hub: Hub) -> tuple[int, int]:
        """
        Calculates the screen position of a hub.

        The hub's original coordinates are scaled and translated so that the
        complete network is centered within the Pygame window.
        """
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
        """
        Updates the visual dimensions used by the renderer.

        The provided values control the map scale, hub size, and drone size
        used when rendering the simulation.
        """
        self.scale = scale
        self.hub_size = hub_size
        self.drone_size = drone_size
