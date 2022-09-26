import sys
from abc import abstractmethod

import peewee as pw
from src.command.command import Command
from src.helper.helperlib import err


class SelectTableCommand(Command):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def _get_table(self) -> pw.ModelBase:
        """returns a table from Peewee Model"""

    def execute(self) -> str:
        return "\n".join(
            ", ".join("{!s}{!r}".format(key, val) for key, val in row.items())
            for row in self._get_table().select().dicts()
        )


class SelectAllCommand(SelectTableCommand):
    def __init__(self, tablename: str) -> None:
        super().__init__()
        self.__table = tablename
        self.err_msg = "The table was not found in the database"

    def _get_table(self) -> pw.ModelBase:
        table = self._app._model.get(self.__table)
        if table:
            return table
        err(self.err_msg)
        sys.stdout.write(str(self))
        sys.exit(1)
