from typing import Optional


class Connection:
    def __init__(self, connection: tuple[str, str], meta_data: Optional[str] = None) -> None:
        self.connection: tuple[str, str] = connection
        self.meta_data: Optional[str] = meta_data
