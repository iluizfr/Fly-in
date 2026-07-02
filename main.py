from src import Parser, ParserError, Graph, Hub, HubError, ConectionError
import sys 


def main() -> None:
    try:
        parser = Parser("map.txt")
        parser.display_parser()

    except (ParserError, ValueError, HubError, ConectionError) as error:
        print(f"Error: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
