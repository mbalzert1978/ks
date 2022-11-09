from __future__ import annotations

from .base import Connection
from .container import (
    Attribute,
    ClassRepresentation,
    ForeignKey,
    Null,
    PrimaryKey,
)


class Creator:
    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    def create_model(self) -> str:
        head = self._get_header()
        body = self._generate_body()
        return "\n".join([head, body])

    def _get_header(self) -> str:
        header = [
            "from __future__ import annotations",
            "from datetime import date",
            "from sqlmodel import SQLModel",
            "from sqlmodel import Field",
        ]
        return "\n".join(header)

    def _get_type(self, value: str) -> str:
        converter = {
            "INTEGER": "int",
            "NVARCHAR": "str",
            "DATETIME": "date",
            "NUMERIC": "str",
        }
        value, _, _ = value.partition("(")
        return converter.get(value, "")

    def _get_tables(self) -> list[tuple[str, ...]]:
        query = (
            "SELECT name FROM sqlite_schema WHERE "
            "type ='table' AND name NOT LIKE 'sqlite_%';"
        )
        return self.connection.fetch_all(query)

    def _get_primary_keys(self, table: str) -> list[tuple[str, ...]]:
        query = (
            "SELECT l.name FROM pragma_table_info('%s') "
            "as l WHERE l.pk <> 0;" % table
        )
        return self.connection.fetch_all(query)

    def _get_foreign_keys(self, table: str) -> list[tuple[str, ...]]:
        query = "SELECT * FROM pragma_foreign_key_list('%s');" % table
        return self.connection.fetch_all(query)

    def _generate_attributes(self, table: str) -> list[Attribute]:
        query = "pragma table_info('%s');" % table
        result = self.connection.fetch_all(query=query)
        primary_cache = {
            name: PrimaryKey(name=name)
            for name, *_ in self._get_primary_keys(table)
        }
        foreign_cache = {
            name: ForeignKey(name=name, from_table=from_table, to=to)
            for _, _, from_table, name, to, *_ in self._get_foreign_keys(table)
        }
        attributes = []
        for _, name, type_, not_null, *_ in result:
            not_null = Null(null=bool(not_null))
            attributes.append(
                Attribute(
                    name=name,
                    type=self._get_type(type_),
                    primary=primary_cache.get(name, PrimaryKey()),
                    foreign=foreign_cache.get(name, ForeignKey()),
                    null=not_null,
                )
            )
        return attributes

    def _generate_body(self) -> str:
        tables = self._get_tables()
        model = []
        for table, *_ in tables:
            result = ClassRepresentation(
                name=table, attributes=self._generate_attributes(table=table)
            )
            model.append(str(result))
        return "\n".join(model)
