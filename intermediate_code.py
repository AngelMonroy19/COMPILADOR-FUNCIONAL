from __future__ import annotations

from ast_nodes import (
    Assignment,
    BinaryExpression,
    Block,
    ComparisonExpression,
    Identifier,
    IfStatement,
    Literal,
    PrintStatement,
    Program,
    VarDeclaration,
)


class IntermediateCodeGenerator:
    def __init__(self) -> None:
        # Acá guardo instrucciones, temporales y etiquetas.
        self.instructions: list[str] = []
        self.temp_counter = 0
        self.label_counter = 0

    def generate(self, program: Program) -> list[str]:
        # Reseteo el estado y genero todo de nuevo.
        self.instructions = []
        self.temp_counter = 0
        self.label_counter = 0

        for statement in program.statements:
            self._gen_statement(statement)
        return self.instructions

    def _gen_statement(self, statement) -> None:
        # Según la sentencia, saco sus instrucciones.
        if isinstance(statement, VarDeclaration):
            value = self._gen_expression(statement.initializer)
            self.instructions.append(f"{statement.name} = {value}")
            return

        if isinstance(statement, Assignment):
            value = self._gen_expression(statement.expression)
            self.instructions.append(f"{statement.name} = {value}")
            return

        if isinstance(statement, PrintStatement):
            value = self._gen_expression(statement.expression)
            self.instructions.append(f"print {value}")
            return

        if isinstance(statement, IfStatement):
            self._gen_if_statement(statement)
            return

        if isinstance(statement, Block):
            for inner_statement in statement.statements:
                self._gen_statement(inner_statement)
            return

        raise ValueError("Unknown statement type for intermediate code generation")

    def _gen_if_statement(self, statement: IfStatement) -> None:
        # El if se traduce con saltos y etiquetas.
        condition_temp = self._gen_expression(statement.condition)
        else_label = self._new_label("L_else")
        end_label = self._new_label("L_end")

        self.instructions.append(f"if_false {condition_temp} goto {else_label}")
        self._gen_statement(statement.then_branch)
        self.instructions.append(f"goto {end_label}")
        self.instructions.append(f"{else_label}:")

        if statement.else_branch is not None:
            self._gen_statement(statement.else_branch)

        self.instructions.append(f"{end_label}:")

    def _gen_expression(self, expression) -> str:
        # Devuelvo un valor directo o el nombre de un temporal.
        if isinstance(expression, Literal):
            return str(expression.value)

        if isinstance(expression, Identifier):
            return expression.name

        if isinstance(expression, BinaryExpression):
            left = self._gen_expression(expression.left)
            right = self._gen_expression(expression.right)
            temp = self._new_temp()
            self.instructions.append(f"{temp} = {left} {expression.operator} {right}")
            return temp

        if isinstance(expression, ComparisonExpression):
            left = self._gen_expression(expression.left)
            right = self._gen_expression(expression.right)
            temp = self._new_temp()
            self.instructions.append(f"{temp} = {left} {expression.operator} {right}")
            return temp

        raise ValueError("Unknown expression type for intermediate code generation")

    def _new_temp(self) -> str:
        # Creo temporales tipo t1, t2, t3...
        self.temp_counter += 1
        return f"t{self.temp_counter}"

    def _new_label(self, prefix: str) -> str:
        # Creo etiquetas nuevas para los saltos.
        self.label_counter += 1
        return f"{prefix}_{self.label_counter}"
