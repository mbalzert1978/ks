from typing import overload


class Base:
    def __init__(self, name, type) -> None:
        self.name = name
        self.type = type

    def __str__(self) -> str:
        return f"{self.name}:{self.type}"


class Field(Base):
    @overload
    def __init__(self, name, type, hook: list[str]) -> None:
        ...

    @overload
    def __init__(self, name, type, hook: str) -> None:
        ...

    def __init__(self, name, type, hook: str | list[str] = "") -> None:
        super().__init__(name, type)
        self.hook = ", ".join(hook) if isinstance(hook, list) else hook

    def __str__(self) -> str:
        return super().__str__() + f"= Field({self.hook})"


class Null(Base):
    @overload
    def __init__(self, name, type, hook: list[str]) -> None:
        ...

    @overload
    def __init__(self, name, type, hook: str) -> None:
        ...

    def __init__(self, name, type, hook: str | list[str] = "") -> None:
        super().__init__(name, type)
        self.hook = ", ".join(hook) if isinstance(hook, list) else hook

    def __str__(self) -> str:
        return (
            super().__str__()
            + f" | None = Field(default=None{', 'if self.hook else ''} {self.hook})"
        )
