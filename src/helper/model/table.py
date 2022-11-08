from dataclasses import dataclass, field
from .base import Null, Field


@dataclass
class PrimaryKey:
    name: str

    def __str__(self) -> str:
        return "primary_key=True"


@dataclass
class ForeignKey:
    name: str
    from_table: str
    to: str

    def __str__(self) -> str:
        return f"foreign_key='{self.from_table}.{self.to}'"


@dataclass
class Attribute:
    name: str
    type: str
    primary_key: PrimaryKey | str
    foreign_key: ForeignKey | str
    not_null: bool = False

    def __str__(self) -> str:
        if self.primary_key:
            return str(
                Null(
                    name=self.name,
                    type=self.type,
                    hook=[str(self.primary_key), str(self.foreign_key)],
                )
            )
        if self.foreign_key and self.not_null:
            return str(
                Field(
                    name=self.name, type=self.type, hook=str(self.foreign_key)
                )
            )
        if self.foreign_key or not self.not_null:
            return str(
                Null(
                    name=self.name, type=self.type, hook=str(self.foreign_key)
                )
            )
        return f"{self.name}:{self.type}"


@dataclass
class TableClass:
    name: str
    attributes: list[Attribute] = field(default_factory=list)

    def __str__(self) -> str:
        return f"class {self.name}(SQLModel, table=True):\n" + "".join(
            f"    {sentence}\n" for sentence in self.attributes
        )
