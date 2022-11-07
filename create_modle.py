from dataclasses import dataclass, field
import re
import sqlite3
from pathlib import Path
import black


DB = Path("database.db")


class Attribute:
    def __init__(self, name, type) -> None:
        self.name = find_one_in_bracket(name)
        self.type = get_type(type)

    def __str__(self) -> str:
        return f"{self.name}:{self.type}"


class NullableAttribute(Attribute):
    def __str__(self, hook: str = "") -> str:
        return super().__str__() + f" | None = Field(default=None{hook})"


class PrimaryKey(NullableAttribute):
    def __str__(self) -> str:
        return super().__str__(hook=", primary_key=True")


class ForeignKeyNullable(NullableAttribute):
    def __str__(self) -> str:
        return super().__str__(hook=", foreign_key=''")


@dataclass
class Container:
    header: str = field(default="")
    attributes: list[str] = field(default_factory=list)


class CommandParser:
    def __init__(self, command: str) -> None:
        self.commands: list[str] = command.splitlines()
        self.pk: dict[str, str] = dict()
        self.fk: dict[str, str] = dict()
        self.parsed: Container

    def setup_container(self) -> None:
        for command in self.commands:
            match command.split():
                case ["CREATE", "TABLE", name]:
                    self.parsed = Container(
                        "class "
                        f"{find_one_in_bracket(name)}(SQLModel, table=True):"
                    )
                case ["FOREIGN", *_]:
                    attr, table, field = find_all_in_bracket(command)
                    self.fk[attr] = f"{table}.{field}"
                case ["CONSTRAINT", _, "PRIMARY", *_]:
                    _, *pk = find_all_in_bracket(command)
                    for item in pk:
                        self.pk[item] = item
                case [_, _, "PRIMARY", *_]:
                    first, *_ = find_all_in_bracket(command)
                    self.pk[first] = first
                case _:
                    continue

    def create_attr(self) -> Container:
        for command in self.commands:
            cmd = command.rstrip(",").strip().split()
            match cmd:
                case [name, type_, *_, "NOT", "NULL"]:
                    self.parsed.attributes.append(
                        self.construct_str(
                            find_one_in_bracket(name),
                            get_type(type_),
                            not_null=True,
                        )
                    )
                case [name, type_]:
                    self.parsed.attributes.append(
                        self.construct_str(
                            find_one_in_bracket(name),
                            get_type(type_),
                        )
                    )
                case _:
                    continue
        return self.parsed

    def construct_str(
        self, name: str, type: str, not_null: bool = False
    ) -> str:
        string_parts = {
            "base": f"{name}: {type}",
            "none": " | None ",
            "field": "= Field(",
            "equals": "= None",
            "default": "default=None",
            "pk": "primary_key=True",
            "fk": "foreign_key=",
            "comma": ", ",
        }
        pk = self.pk.get(name, "")
        fk = self.fk.get(name, "")
        string = string_parts.get("base", "")
        match (bool(pk), bool(fk), not_null):
            case (True, True, True | False):
                string += string_parts.get("none", "")
                string += string_parts.get("field", "")
                string += string_parts.get("default", "")
                string += string_parts.get("comma", "")
                string += string_parts.get("pk", "")
                string += string_parts.get("comma", "")
                string += string_parts.get("fk", "")
                string += f"'{fk}'"
                string += ")"
                return string
            case (True, False, True | False):
                string += string_parts.get("none", "")
                string += string_parts.get("field", "")
                string += string_parts.get("default", "")
                string += string_parts.get("comma", "")
                string += string_parts.get("pk", "")
                string += ")"
                return string
            case (False, True, False):
                string += string_parts.get("none", "")
                string += string_parts.get("field", "")
                string += string_parts.get("default", "")
                string += string_parts.get("comma", "")
                string += string_parts.get("fk", "")
                string += f"'{fk}'"
                string += ")"
                return string
            case (False, True, True):
                string += string_parts.get("field", "")
                string += string_parts.get("fk", "")
                string += f"'{fk}'"
                string += ")"
                return string
            case (False, False, False):
                string += string_parts.get("none", "")
                string += string_parts.get("field", "")
                string += string_parts.get("default", "")
                string += ")"
                return string
            case _:
                return string_parts.get("base", "")


def main():
    create_by_creation_str()


def create_by_creation_str():
    get_fks_cmd = "SELECT sql  FROM (SELECT sql sql, type type, tbl_name tbl_name, name name FROM sqlite_master UNION ALL SELECT sql, type, tbl_name, name FROM sqlite_temp_master) WHERE type != 'meta' AND sql NOTNULL AND name NOT LIKE 'sqlite_%' ORDER BY substr(type, 2, 1), name"
    con = sqlite3.connect(DB)
    cursor = con.cursor()
    result: list[tuple[str]] = cursor.execute(get_fks_cmd).fetchall()
    body: list[Container] = []
    for command in result:
        command, *_ = command
        if "TABLE" not in command:
            continue
        parser = CommandParser(command)
        parser.setup_container()
        body.append(parser.create_attr())
    file_str = format_file(body)
    with open("test_model.py", "w") as file:
        file.write(file_str)


def format_file(body: list[Container]) -> str:
    outstring = ""
    newline = "\n"
    for item in get_header():
        outstring += item
        outstring += newline
    for item in body:
        outstring += item.header
        outstring += newline
        for attr in item.attributes:
            outstring += " " * 4
            outstring += attr
            outstring += newline
    file_str = black.format_str(outstring, mode=black.Mode())
    return file_str


def find_one_in_bracket(value) -> str:
    all = find_all_in_bracket(value)
    if not all:
        return ""
    first, *_ = all
    return first


def find_all_in_bracket(value) -> list[str]:
    find = r"\[(.*?)\]"
    return re.findall(find, value)


def get_header() -> list[str]:
    return [
        "from __future__ import annotations",
        "from datetime import date",
        "from sqlmodel import SQLModel",
        "from sqlmodel import Field",
    ]


def get_type(value: str) -> str:
    converter = {
        "INTEGER": "int",
        "NVARCHAR": "str",
        "DATETIME": "date",
        "NUMERIC": "str",
    }
    value, _, _ = value.partition("(")
    return converter.get(value, "")


if __name__ == "__main__":
    main()
