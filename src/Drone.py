class Drone:
    def __init__(self, id: str) -> None:
        self.id = id
        self.path = []
        self.remaining_turns = 0
        self.finished = False

        self.current_hub = None
        self.current_connection = None
        self.destinatiom_hub = None
        self.just_arrived = False

    def __repr__(self) -> str:
        return self.id
