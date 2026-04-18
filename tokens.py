from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    INT = auto()
    IF = auto()
    ELSE = auto()
    PRINT = auto()
    IDENTIFIER = auto()
    INTEGER = auto()
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    ASSIGN = auto()
    EQUAL_EQUAL = auto()
    LESS = auto()
    GREATER = auto()
    SEMICOLON = auto()
    LBRACE = auto()
    RBRACE = auto()
    LPAREN = auto()
    RPAREN = auto()
    EOF = auto()


@dataclass(frozen=True)
class Token:
    type: TokenType
    lexeme: str
    literal: int | None
    line: int
    column: int

    def __str__(self) -> str:
        # Este formato es el que se muestra por pantalla.
        literal_part = f", literal={self.literal}" if self.literal is not None else ""
        return f"{self.type.name}('{self.lexeme}'{literal_part}) @ {self.line}:{self.column}"
