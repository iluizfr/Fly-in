import os


class Menu:
    def __init__(self) -> None:
        self.scale = 100
        self.drone_size = 8
        self.hub_size = 20

    def display(self) -> str:
        print("=" * 20)
        print("Fly-in")

        print("\nChoose difficult:")
        print("challenger\neasy\nhard\nmedium")
        dif = input("\nchoice: ")

        if dif == "hard":
            self.scale = 80

        elif dif == "challenger":
            self.scale = 40
            self.drone_size = 4
            self.hub_size = 11

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

    def get_info(self) -> tuple[int, int, int]:
        return (self.scale, self.hub_size, self.drone_size)
