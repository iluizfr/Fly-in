from src import Parser, ParserError, Graph, HubError, ConectionError
from src import Simulator, Renderer, Menu
import pygame
import sys


def main() -> None:
    try:
        menu = Menu()
        path: str = menu.display()
        parser = Parser(path)
        graph = Graph(parser)
        simulator = Simulator(graph)
        renderer = Renderer(simulator)

        scale, hub_size, drone_size = menu.get_info()
        renderer.set_sizes(scale, hub_size, drone_size)
        clock = pygame.time.Clock()

        print(f"Number of drones: {len(graph.drones)}\n")

        while renderer.running and simulator.drones:
            renderer.update()
            renderer.draw()
            simulator.simulate_turn()
            clock.tick(1)

        print(f"\nTurnos: {simulator.current_turn}")
        print("=" * 20)

    except (ParserError, ValueError, HubError, ConectionError,
            PermissionError, FileNotFoundError, IndexError) as error:
        print(f"\n{error}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
