from typing import Generator

from .table import Attribute, ForeignKey, PrimaryKey, TableClass
from .db_connection import query_get_all


def get_model_str(db: str) -> str:
    global DB
    DB = db
    return_str = ""
    for head in get_header():
        return_str += head
        return_str += "\n"
    for class_ in get_tables():
        class_.attributes = list(generate_attributes(class_.name))
        return_str += str(class_)
    return return_str


def get_tables() -> Generator[TableClass, None, None]:
    query = (
        "SELECT name FROM sqlite_schema WHERE "
        "type ='table' AND name NOT LIKE 'sqlite_%';"
    )
    result = query_get_all(DB, query)
    for table in result:
        name, *_ = table
        yield TableClass(name=name)


def get_pks(table: str) -> Generator[PrimaryKey, None, None]:
    query = (
        "SELECT l.name FROM pragma_table_info('%s') "
        "as l WHERE l.pk <> 0;" % table
    )
    result = query_get_all(DB, query)
    for pk in result:
        name, *_ = pk
        yield PrimaryKey(name=name)


def get_fks(table: str) -> Generator[ForeignKey, None, None]:
    query = "SELECT * FROM pragma_foreign_key_list('%s');" % table
    result = query_get_all(DB, query)
    for fk in result:
        _, _, from_table, name, to, *_ = fk
        yield ForeignKey(name=name, from_table=from_table, to=to)


def generate_attributes(table: str) -> Generator[Attribute, None, None]:
    query = "pragma table_info('%s');" % table
    result = query_get_all(DB, query)
    for field in result:
        _, name, type_, not_null, *_ = field
        pk = next((obj for obj in get_pks(table) if obj.name == name), "")
        fk = next((obj for obj in get_fks(table) if obj.name == name), "")
        yield Attribute(
            name=name,
            type=get_type(type_),
            not_null=bool(not_null),
            primary_key=pk,
            foreign_key=fk,
        )


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
    exit()
