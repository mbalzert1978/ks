import json
from typing import TYPE_CHECKING

from ..helper.helperlib import fix_suffix, str_to_path, create_file

if TYPE_CHECKING:
    from pathlib import Path

    from sqlmodel import SQLModel


class JsonWriter:
    def __init__(self, data: list["SQLModel"]) -> None:
        self._subsystem = json
        self._data = data

    def write(self, filename: str) -> None:
        filename = fix_suffix(filename, ".json")
        file: "Path" = str_to_path(filename)
        create_file(file)
        json.dump(
            list(x.dict() for x in self._data), fp=file.open("w"), indent=4
        )
