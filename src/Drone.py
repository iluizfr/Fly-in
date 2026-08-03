class Drone:
    def __init__(self, id: str) -> None:
        self.id = id
        self.current_hub = None
        self.current_connection = None
        self.path = []
        self.path_index = 0
        self.remaining_turns = 0
        self.finished = False
        self.just_arrived = False

    def __repr__(self) -> str:
        return self.id
