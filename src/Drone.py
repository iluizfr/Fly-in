from typing import TYPE_CHECKING


# Just to pass mypy errors
if TYPE_CHECKING:
    from .Hub import Hub
    from .Connection import Connection


class Drone:
    """
    Represents a drone moving through the network of hubs and connections.

    The drone keeps track of its route, current location, destination, and
    movement state during the simulation.
    """

    def __init__(self, id: str) -> None:
        """
        Initializes a drone with the given identifier.
        """
        self.id: str = id
        self.path: list[Hub] = []
        self.remaining_turns: int = 0
        self.finished: bool = False

        self.current_hub: Hub | None = None
        self.current_connection: Connection | None = None
        self.destination_hub: Hub | None = None
        self.just_arrived: bool = False

    def __repr__(self) -> str:
        """
        Returns a string representation of the drone.

        The drone is represented by its unique id.
        """
        return self.id
