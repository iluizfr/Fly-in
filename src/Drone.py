from src.Hub import Hub
from src.Connection import Connection


class Drone:
    def __init__(self, id: str) -> None:
        self.id: str = id
        self.path: list[Hub] = []
        self.remaining_turns: int = 0
        self.finished: bool = False

        self.current_hub: Hub | None = None
        self.current_connection: Connection | None = None
        self.destination_hub: Hub | None = None
        self.just_arrived: bool = False

    def __repr__(self) -> str:
        return self.id
