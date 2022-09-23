from abc import ABC, abstractmethod
import sys
from typing import Any, Optional


class Command(ABC):
    def __init__(self) -> None:
        super().__init__()
        self.err_msg: Optional[str] = None

    def _set_app(self, app: Any) -> None:
        self._app = app

    def err(self) -> None:
        sys.stderr.write("\033[91m%s\033[0m\n" % self.err_msg)
        sys.stderr.flush()

    @abstractmethod
    def execute(self) -> Optional[Any]:
        """Command to execute"""
