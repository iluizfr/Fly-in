import os


class Menu:
    def __init__(self) -> None:
        self.scale = 100
        self.drone_size = 8
        self.hub_size = 20

    def __repr__(self) -> str:
        return "Menu"

    def display(self) -> str:
        print("=" * 20)
        print("Fly-in")

        print("\nChoose difficult:")
        print("easy\nmedium\nhard\nchallenger")
        dif = input("\nchoice: ")

        if dif == "easy":
            self.scale = 120
            self.drone_size = 13

        elif dif == "hard":
            self.scale = 70
            self.drone_size = 13

        elif dif == "medium":
            self.scale = 120
            self.drone_size = 13

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

        if mapa == "02_the_fractured.txt":
            self.scale = 20
        print()

        return f"maps/{dif}/{mapa}"

    def get_info(self) -> tuple[int, int, int]:
        return (self.scale, self.hub_size, self.drone_size)
