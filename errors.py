from __future__ import annotations


class CompilerError(Exception):
    """Clase base para los errores de las fases del compilador."""


class LexicalError(CompilerError):
    def __init__(self, message: str, line: int, column: int) -> None:
        # Armo el mensaje del error léxico.
        super().__init__(f"Error léxico en {line}:{column} -> {message}")
        self.line = line
        self.column = column


class SyntaxError(CompilerError):
    def __init__(self, message: str, line: int, column: int) -> None:
        # Armo el mensaje del error sintáctico.
        super().__init__(f"Error sintáctico en {line}:{column} -> {message}")
        self.line = line
        self.column = column


class SemanticError(CompilerError):
    def __init__(self, message: str, line: int, column: int) -> None:
        # Armo el mensaje del error semántico.
        super().__init__(f"Error semántico en {line}:{column} -> {message}")
        self.line = line
        self.column = column
