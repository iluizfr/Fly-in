from src import Parser, ParserError, Graph, HubError, ConectionError
from src import Simulator
import sys, os
from pathlib import Path
import shutil


def menu() -> str:
    os.system("clear")
    print("=" * 20)
    print("Fly-in")

    print("Choose difficult:")
    print("challenger\neasy\nhard\nmedium")
    dif = input("choice: ")

    filles = os.listdir(f"maps/{dif}")
    os.system("clear")
    print("=" * 20)
    print("Fly-in")
    print("Choose the map:")

    for map in filles:
        print(map)
    mapa = input("map: ")

    ori = Path(f"maps/{dif}/{mapa}")
    dest = Path(f"../../{mapa}")
    shutil.copy(ori, dest)

    return mapa


def main() -> None:
    try:
        parser = Parser(menu())
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
