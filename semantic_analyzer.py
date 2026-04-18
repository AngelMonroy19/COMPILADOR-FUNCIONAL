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
from errors import SemanticError
from symbol_table import Symbol, SymbolTable


class SemanticAnalyzer:
    def __init__(self) -> None:
        # Arranco con la tabla de símbolos.
        self.symbol_table = SymbolTable()

    def analyze(self, program: Program) -> SymbolTable:
        # Reviso todas las sentencias del programa.
        for statement in program.statements:
            self._analyze_statement(statement)
        return self.symbol_table

    def _analyze_statement(self, statement) -> None:
        # Según la sentencia, la mando al chequeo que toca.
        if isinstance(statement, VarDeclaration):
            self._analyze_var_declaration(statement)
        elif isinstance(statement, Assignment):
            self._analyze_assignment(statement)
        elif isinstance(statement, PrintStatement):
            self._analyze_expression(statement.expression)
        elif isinstance(statement, IfStatement):
            self._analyze_if_statement(statement)
        elif isinstance(statement, Block):
            self._analyze_block(statement)
        else:
            raise SemanticError("Tipo de sentencia desconocido", 0, 0)

    def _analyze_var_declaration(self, statement: VarDeclaration) -> None:
        # No dejo redeclarar en el mismo bloque.
        if self.symbol_table.declared_in_current_scope(statement.name):
            raise SemanticError(
                f"La variable '{statement.name}' ya fue declarada en este bloque",
                statement.line,
                statement.column,
            )

        self._analyze_expression(statement.initializer)
        self.symbol_table.declare(
            Symbol(
                name=statement.name,
                var_type="int",
                declared_line=statement.line,
                declared_column=statement.column,
                initialized=True,
            )
        )

    def _analyze_assignment(self, statement: Assignment) -> None:
        # La variable tiene que existir antes de asignarle algo.
        symbol = self.symbol_table.resolve(statement.name)
        if symbol is None:
            raise SemanticError(
                f"La variable '{statement.name}' no fue declarada",
                statement.line,
                statement.column,
            )

        self._analyze_expression(statement.expression)
        symbol.initialized = True

    def _analyze_if_statement(self, statement: IfStatement) -> None:
        # La condición del if tiene que dar bool.
        condition_type = self._analyze_expression(statement.condition)
        if condition_type != "bool":
            raise SemanticError(
                "La condición del if tiene que ser una comparación",
                statement.line,
                statement.column,
            )
        self._analyze_statement(statement.then_branch)
        if statement.else_branch is not None:
            self._analyze_statement(statement.else_branch)

    def _analyze_block(self, block: Block) -> None:
        # Entro a un ámbito nuevo para el bloque.
        self.symbol_table.enter_scope()
        for statement in block.statements:
            self._analyze_statement(statement)
        self.symbol_table.exit_scope()

    def _analyze_expression(self, expression) -> str:
        # Devuelvo el tipo de la expresión.
        if isinstance(expression, Literal):
            return "int"

        if isinstance(expression, Identifier):
            symbol = self.symbol_table.resolve(expression.name)
            if symbol is None:
                raise SemanticError(
                    f"La variable '{expression.name}' no fue declarada",
                    expression.line,
                    expression.column,
                )
            if not symbol.initialized:
                raise SemanticError(
                    f"La variable '{expression.name}' se usa antes de inicializarse",
                    expression.line,
                    expression.column,
                )
            return symbol.var_type

        if isinstance(expression, BinaryExpression):
            left_type = self._analyze_expression(expression.left)
            right_type = self._analyze_expression(expression.right)

            if left_type != "int" or right_type != "int":
                raise SemanticError(
                    "Las operaciones aritméticas solo trabajan con enteros",
                    expression.line,
                    expression.column,
                )
            return "int"

        if isinstance(expression, ComparisonExpression):
            left_type = self._analyze_expression(expression.left)
            right_type = self._analyze_expression(expression.right)

            if left_type != "int" or right_type != "int":
                raise SemanticError(
                    "Las comparaciones solo trabajan con enteros",
                    expression.line,
                    expression.column,
                )
            return "bool"

        raise SemanticError("Tipo de expresión desconocido", 0, 0)
