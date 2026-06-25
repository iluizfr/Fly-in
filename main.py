from src import Parser, ParserError, Graph, Hub
import sys 


def display_parser(parser: Parser) -> None:
    print(f"nb_drone: {parser.nb_drones}\n")
    print("start_hub:")
    print(f"    name: {parser.start_hub.name}")
    print(f"    pos: {parser.start_hub.pos}")
    print(f"    meta data: {parser.start_hub.meta_data}\n")

    print("Hubs:")
    for hub in parser.hubs:
        print(f"    name: {hub.name}")
        print(f"    pos: {hub.pos}")
        print(f"    meta data: {hub.meta_data}\n")

    print("end_hub:")
    print(f"    name: {parser.end_hub.name}")
    print(f"    pos: {parser.end_hub.pos}")
    print(f"    meta data: {parser.end_hub.meta_data}\n")

    print("Connections:")
    for connection in parser.connections:
        print(f"    Connection: {connection.connection}")
        print(f"    meta data: {connection.meta_data}\n")


def main() -> None:
    try:
        parser = Parser("map.txt")
        display_parser(parser)


    except (ParserError, ValueError) as error:
        print(f"Error: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
