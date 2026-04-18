from __future__ import annotations

from dataclasses import dataclass, field


class ASTNode:
    def pretty(self, indent: int = 0) -> str:
        # Cada nodo se imprime a su manera.
        raise NotImplementedError


class Stmt(ASTNode):
    pass


class Expr(ASTNode):
    pass


@dataclass
class Program(ASTNode):
    statements: list[Stmt] = field(default_factory=list)

    def pretty(self, indent: int = 0) -> str:
        # Imprime el programa completo.
        pad = "  " * indent
        children = "\n".join(stmt.pretty(indent + 1) for stmt in self.statements)
        return f"{pad}Program\n{children}" if children else f"{pad}Program"


@dataclass
class Block(Stmt):
    statements: list[Stmt]
    line: int
    column: int

    def pretty(self, indent: int = 0) -> str:
        # Imprime el bloque con sus sentencias.
        pad = "  " * indent
        children = "\n".join(stmt.pretty(indent + 1) for stmt in self.statements)
        return f"{pad}Block\n{children}" if children else f"{pad}Block"


@dataclass
class VarDeclaration(Stmt):
    name: str
    initializer: Expr
    line: int
    column: int

    def pretty(self, indent: int = 0) -> str:
        # Imprime la declaración y su valor inicial.
        pad = "  " * indent
        return f"{pad}VarDeclaration(name={self.name})\n{self.initializer.pretty(indent + 1)}"


@dataclass
class Assignment(Stmt):
    name: str
    expression: Expr
    line: int
    column: int

    def pretty(self, indent: int = 0) -> str:
        # Imprime la asignación.
        pad = "  " * indent
        return f"{pad}Assignment(name={self.name})\n{self.expression.pretty(indent + 1)}"


@dataclass
class PrintStatement(Stmt):
    expression: Expr
    line: int
    column: int

    def pretty(self, indent: int = 0) -> str:
        # Imprime la instrucción print.
        pad = "  " * indent
        return f"{pad}Print\n{self.expression.pretty(indent + 1)}"


@dataclass
class IfStatement(Stmt):
    condition: Expr
    then_branch: Stmt
    else_branch: Stmt | None
    line: int
    column: int

    def pretty(self, indent: int = 0) -> str:
        # Imprime el if completo.
        pad = "  " * indent
        result = [f"{pad}If"]
        result.append(f"{pad}  Condition:")
        result.append(self.condition.pretty(indent + 2))
        result.append(f"{pad}  Then:")
        result.append(self.then_branch.pretty(indent + 2))
        if self.else_branch is not None:
            result.append(f"{pad}  Else:")
            result.append(self.else_branch.pretty(indent + 2))
        return "\n".join(result)


@dataclass
class BinaryExpression(Expr):
    left: Expr
    operator: str
    right: Expr
    line: int
    column: int

    def pretty(self, indent: int = 0) -> str:
        # Imprime una operación aritmética.
        pad = "  " * indent
        return (
            f"{pad}Binary(op={self.operator})\n"
            f"{self.left.pretty(indent + 1)}\n"
            f"{self.right.pretty(indent + 1)}"
        )


@dataclass
class ComparisonExpression(Expr):
    left: Expr
    operator: str
    right: Expr
    line: int
    column: int

    def pretty(self, indent: int = 0) -> str:
        # Imprime una comparación.
        pad = "  " * indent
        return (
            f"{pad}Comparison(op={self.operator})\n"
            f"{self.left.pretty(indent + 1)}\n"
            f"{self.right.pretty(indent + 1)}"
        )


@dataclass
class Literal(Expr):
    value: int
    line: int
    column: int

    def pretty(self, indent: int = 0) -> str:
        # Imprime el número literal.
        pad = "  " * indent
        return f"{pad}Literal({self.value})"


@dataclass
class Identifier(Expr):
    name: str
    line: int
    column: int

    def pretty(self, indent: int = 0) -> str:
        # Imprime el nombre de la variable.
        pad = "  " * indent
        return f"{pad}Identifier({self.name})"
