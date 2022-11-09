from typing import Protocol


class Connection(Protocol):
    def _is_valid_db(self, value: str) -> bool:
        ...

    def fetch_all(self, query: str) -> list[tuple[str, ...]]:
        ...

    def fetch_one(self, query: str) -> tuple[str, ...]:
        ...
