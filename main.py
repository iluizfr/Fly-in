from src import parser, ParserError, Graph, Node
import sys 


def main() -> None:
    try:
        config = parser("map.txt")
        graph = Graph()
        node = Node(config["start_hub"]["name"], config["start_hub"]["coordenate"], config["start_hub"]["meta_data"])
        graph.add_node(node)
        graph.info()

    except (ParserError, ValueError) as error:
        print(f"Error: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
