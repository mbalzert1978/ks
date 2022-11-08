from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class TableClass:
    name: str
    attributes: list[Attribute] = field(default_factory=list)

    def __str__(self) -> str:
        return f"class {self.name}(SQLModel, table=True):\n" + "".join(
            f"    {sentence}\n" for sentence in self.attributes
        )


@dataclass
class Attribute:
    name: str
    type: str

    def __str__(self) -> str:
        return f"{self.name}:{self.type}"


class FieldBase(Attribute):
    def __str__(self, hook: str = "") -> str:
        base = f" = Field({hook})"
        return super().__str__() + base


class NullBase(Attribute):
    def __str__(self, hook: str = "") -> str:
        base = f" | None = Field(default=None, {hook})"
        return super().__str__() + base


@dataclass
class PrimaryKey(NullBase):
    def __str__(self, hook: str = "") -> str:
        base = f"primary_key=True{hook}"
        return super().__str__(hook=base)


@dataclass
class NullForeignKey(NullBase):
    from_table: str = field(repr=False)
    to: str = field(repr=False)

    def __str__(self) -> str:
        base = f"foreign_key='{self.from_table}.{self.to}'"
        return super().__str__(hook=base)


@dataclass
class PrimaryWithForeignKey(PrimaryKey):
    from_table: str = field(repr=False)
    to: str = field(repr=False)

    def __str__(self) -> str:
        base = f", foreign_key='{self.from_table}.{self.to}'"
        return super().__str__(hook=base)


@dataclass
class ForeignKey(FieldBase):
    from_table: str = field(repr=False)
    to: str = field(repr=False)

    def __str__(self) -> str:
        base = f"foreign_key='{self.from_table}.{self.to}'"
        return super().__str__(hook=base)
