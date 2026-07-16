import pygame
from .Graph import Graph


class Render:
    def __init__(self, graph: Graph):
        self.graph = graph

    def run(self):
        #pygame.init()
        WIDTH = 1200
        HEIGHT = 900

        screan = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Fly-in")

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            pygame.draw.circle(screan, (255, 0, 0), (400, 300), (50))

            pygame.display.flip()

        pygame.quit()
