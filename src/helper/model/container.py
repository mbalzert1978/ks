from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ClassRepresentation:
    name: str
    attributes: list[Attribute] = field(default_factory=list)

    def __str__(self) -> str:
        base = f"class {self.name}(SQLModel, table=True):\n"
        attributes = "".join(
            f"    {sentence}\n" for sentence in self.attributes
        )
        return base + attributes


@dataclass
class PrimaryKey:
    name: str = field(default="")

    def get(self) -> str:
        if self.name:
            return "primary_key=True"
        return ""


@dataclass
class Null:
    null: bool = field(default=False)

    def get(self) -> str:
        if self.null:
            return ""
        return "default=None"


@dataclass
class ForeignKey:
    name: str = field(default="")
    from_table: str = field(default="", repr=False)
    to: str = field(default="", repr=False)

    def get(self) -> str:
        if self.name:
            return f"foreign_key='{self.from_table}.{self.to}'"
        return ""


@dataclass
class Attribute:
    name: str
    type: str
    null: Null = field(default_factory=Null)
    primary: PrimaryKey = field(default_factory=PrimaryKey)
    foreign: ForeignKey = field(default_factory=ForeignKey)

    def __str__(self) -> str:
        type = self.get_type()
        field_value = self.get_field()
        return ":".join([self.name, type]) + field_value

    def get_type(self) -> str:
        none_str = " | None"
        if self.primary.name:
            self.null.null = False
        if not self.null.null:
            return self.type + none_str
        return self.type

    def get_field(self) -> str:
        parts = []
        for item in [self.null, self.primary, self.foreign]:
            part = item.get()
            if not part:
                continue
            parts.append(part)
        if any(parts):
            return f" = Field({', '.join(parts)})"
        return ""
