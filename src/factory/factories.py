from typing import Protocol

from src.command.show_table_command import SelectAllCommand


class Creator(Protocol):
    @staticmethod
    def factor_method(*args):
        """create a product"""


class CreateSelectTable(Creator):
    @staticmethod
    def factor_method(*args):
        return SelectAllCommand(*args)
