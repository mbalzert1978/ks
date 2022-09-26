from abc import ABC, abstractmethod
from typing import Any, Optional


class Command(ABC):
    def __init__(self) -> None:
        super().__init__()

    def _set_app(self, app: Any) -> None:
        self._app = app

    @abstractmethod
    def execute(self) -> Optional[Any]:
        """Command to execute"""
