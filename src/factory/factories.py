from typing import Protocol

from src.command.show_table_command import SelectCommand


class Creator(Protocol):
    @staticmethod
    def factor_method(*args):
        """create a product"""


class CreateSelectTable(Creator):
    @staticmethod
    def factor_method(*args):
        return SelectCommand(*args)
