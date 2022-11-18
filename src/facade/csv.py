import csv
from typing import TYPE_CHECKING

from ..helper.helperlib import create_file, fix_suffix, str_to_path

if TYPE_CHECKING:
    from pathlib import Path

    from sqlmodel import SQLModel


class CsvWriter:
    def __init__(self, data: list["SQLModel"]) -> None:
        self._subsystem = csv
        self._data = data

    def write(self, filename: str, delimiter: str = ";") -> None:
        filename = fix_suffix(filename, ".csv")
        file: "Path" = str_to_path(filename)
        create_file(file)
        with file.open("w") as csvfile:
            writer = self._subsystem.DictWriter(
                csvfile,
                fieldnames=self._get_header(),
                delimiter=delimiter,
            )
            writer.writeheader()
            writer.writerows(x.dict() for x in self._data)

    def _get_header(self) -> dict:
        first = next(iter(self._data), None)
        if first is None:
            return {}
        return first.schema().get("properties", {})
