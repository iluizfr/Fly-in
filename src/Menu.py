import os


class Menu:
    """
    Handles the initial configuration of the simulation.

    The menu allows the user to select a difficulty level and a map. It also
    configures the visual scale and the size of drones and hubs according to
    the selected difficulty.
    """

    def __init__(self) -> None:
        """
        Initializes the menu with the default display settings.
        """
        self.scale = 100
        self.drone_size = 8
        self.hub_size = 20

    def __repr__(self) -> str:
        """
        Returns a string representation of the menu.
        """
        return "Menu"

    def display(self) -> str:
        """
        Displays the menu and handles the user's configuration choices.

        The user selects a difficulty level and a map from the available
        options. The display settings are adjusted according to the selected
        difficulty, and the path to the selected map is returned.
        """
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
        """
        Returns the current display configuration.

        The returned values contain the map scale, hub size, and drone size
        configured by the selected difficulty and map.
        """
        return (self.scale, self.hub_size, self.drone_size)
