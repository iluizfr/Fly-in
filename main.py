from src import Parser, ParserError, Graph, HubError, ConectionError
from src import Simulator
import sys 


def main() -> None:
    try:
        parser = Parser("map.txt")
        graph = Graph(parser)


        simulator = Simulator(graph)
        simulator.simulate()


        #render = Render(graph)
        #render.run()


    except (ParserError, ValueError, HubError, ConectionError) as error:
        print(f"Error: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
