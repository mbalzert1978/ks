import csv
import inspect
from pathlib import Path
from typing import Optional

import peewee as pw
from src.helper.helperlib import (
    create_file,
    extract_header,
    fix_file_extension_csv,
)


class SQLiteDataBase:
    def __init__(self, commands: dict, model) -> None:
        self.__commands = commands
        self.__set_model(model)
        self.__set_commands()

    def _raise(self, ex):
        """
        raises the given Exception
        :ex:`Exception`
        """
        raise ex

    def __set_commands(self) -> None:
        for command in self.__commands.values():
            command._set_app(self)

    def __set_model(self, model) -> None:
        self._model = {
            name: obj
            for name, obj in inspect.getmembers(model)
            if isinstance(obj, pw.ModelBase)
            and not name.startswith(("Sqlite", "BaseM", "Model"))
        }

    def __str__(self) -> str:
        return "\n".join(list(self._model))

    def __repr__(self) -> str:
        return str(list(self._model))

    def select_all_table(self) -> Optional[str]:
        return self.__commands.get(
            "select_all_table", lambda: self._raise(NotImplementedError)
        ).execute()

    def write_csv(self, filename: str, delimiter: str) -> None:
        filename = fix_file_extension_csv(filename)
        table = self.__commands.get(
            "select_all_table", lambda: self._raise(NotImplementedError)
        )._get_table()
        header = extract_header(table)
        file = Path(filename)
        create_file(file)
        with file.open("w") as csvfile:
            writer = csv.DictWriter(csvfile, header, delimiter=delimiter)
            writer.writeheader()
            for row in table.select().dicts():
                writer.writerow(row)
