from src import Parser, ParserError, Graph, HubError, ConectionError
from src import Simulator
import sys, os


def menu() -> str:
    print("=" * 20)
    print("Fly-in")

    print("\nChoose difficult:")
    print("challenger\neasy\nhard\nmedium")
    dif = input("\nchoice: ")

    filles = os.listdir(f"maps/{dif}")
    print("\nChoose the map:")

    i = 1
    for map in filles:
        print(f"{i}: {map}")
        i += 1
    n = int(input("\nmap: "))
    n -= 1
    mapa = filles[n]
    print()

    return f"maps/{dif}/{mapa}"


def main() -> None:
    try:
        parser = Parser(menu())
        graph = Graph(parser)

        simulator = Simulator(graph)
        simulator.simulate()
        print(f"\nTurnos: {simulator.current_turn}")

        #render = Render(graph)
        #render.run()

    except (ParserError, ValueError, HubError, ConectionError) as error:
        print(f"Error: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
