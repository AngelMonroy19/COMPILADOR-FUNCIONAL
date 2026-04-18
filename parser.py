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
    Stmt,
    VarDeclaration,
)
from errors import SyntaxError
from tokens import Token, TokenType


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        # Arranco con la lista de tokens y el cursor en cero.
        self.tokens = tokens
        self.current = 0

    def parse(self) -> Program:
        # Este es el arranque del parser.
        statements: list[Stmt] = []
        while not self._is_at_end():
            statements.append(self._statement())
        return Program(statements)

    def _statement(self) -> Stmt:
        # Según el token actual, veo qué tipo de sentencia viene.
        if self._match(TokenType.INT):
            return self._var_declaration()
        if self._match(TokenType.IF):
            return self._if_statement()
        if self._match(TokenType.PRINT):
            return self._print_statement()
        if self._match(TokenType.LBRACE):
            return self._block()
        if self._check(TokenType.IDENTIFIER):
            return self._assignment_statement()

        token = self._peek()
        raise SyntaxError(
            f"Unexpected token '{token.lexeme or token.type.name}' in statement",
            token.line,
            token.column,
        )

    def _var_declaration(self) -> VarDeclaration:
        # Parsea algo como: int x = ...;
        name_token = self._consume(TokenType.IDENTIFIER, "Expected identifier after 'int'")
        self._consume(TokenType.ASSIGN, "Expected '=' in variable declaration")
        initializer = self._expression()
        self._consume(TokenType.SEMICOLON, "Expected ';' after variable declaration")
        return VarDeclaration(name_token.lexeme, initializer, name_token.line, name_token.column)

    def _assignment_statement(self) -> Assignment:
        # Parsea una asignación común.
        name_token = self._consume(TokenType.IDENTIFIER, "Expected identifier in assignment")
        self._consume(TokenType.ASSIGN, "Expected '=' in assignment")
        expression = self._expression()
        self._consume(TokenType.SEMICOLON, "Expected ';' after assignment")
        return Assignment(name_token.lexeme, expression, name_token.line, name_token.column)

    def _print_statement(self) -> PrintStatement:
        # Parsea la llamada a print(...).
        keyword = self._previous()
        self._consume(TokenType.LPAREN, "Expected '(' after 'print'")
        expression = self._expression()
        self._consume(TokenType.RPAREN, "Expected ')' after print expression")
        self._consume(TokenType.SEMICOLON, "Expected ';' after print statement")
        return PrintStatement(expression, keyword.line, keyword.column)

    def _if_statement(self) -> IfStatement:
        # Acá armo el if y, si está, también el else.
        keyword = self._previous()
        self._consume(TokenType.LPAREN, "Expected '(' after 'if'")
        condition = self._expression()
        self._consume(TokenType.RPAREN, "Expected ')' after if condition")
        then_branch = self._statement()

        else_branch = None
        if self._match(TokenType.ELSE):
            else_branch = self._statement()

        return IfStatement(condition, then_branch, else_branch, keyword.line, keyword.column)

    def _block(self) -> Block:
        # Junta todas las sentencias que están entre llaves.
        opening = self._previous()
        statements: list[Stmt] = []

        while not self._check(TokenType.RBRACE) and not self._is_at_end():
            statements.append(self._statement())

        self._consume(TokenType.RBRACE, "Expected '}' after block")
        return Block(statements, opening.line, opening.column)

    def _expression(self):
        # Entrada general para expresiones.
        return self._equality()

    def _equality(self):
        # Maneja ==.
        expr = self._comparison()
        while self._match(TokenType.EQUAL_EQUAL):
            operator = self._previous()
            right = self._comparison()
            expr = BinaryExpression(expr, operator.lexeme, right, operator.line, operator.column)
        return expr

    def _comparison(self):
        # Maneja < y >.
        expr = self._term()
        while self._match(TokenType.LESS, TokenType.GREATER):
            operator = self._previous()
            right = self._term()
            expr = ComparisonExpression(expr, operator.lexeme, right, operator.line, operator.column)
        return expr

    def _term(self):
        # Maneja + y -.
        expr = self._factor()
        while self._match(TokenType.PLUS, TokenType.MINUS):
            operator = self._previous()
            right = self._factor()
            expr = BinaryExpression(expr, operator.lexeme, right, operator.line, operator.column)
        return expr

    def _factor(self):
        # Maneja * y /.
        expr = self._primary()
        while self._match(TokenType.STAR, TokenType.SLASH):
            operator = self._previous()
            right = self._primary()
            expr = BinaryExpression(expr, operator.lexeme, right, operator.line, operator.column)
        return expr

    def _primary(self):
        # Acá caen números, nombres o expresiones entre paréntesis.
        if self._match(TokenType.INTEGER):
            token = self._previous()
            return Literal(token.literal if token.literal is not None else 0, token.line, token.column)

        if self._match(TokenType.IDENTIFIER):
            token = self._previous()
            return Identifier(token.lexeme, token.line, token.column)

        if self._match(TokenType.LPAREN):
            expr = self._expression()
            self._consume(TokenType.RPAREN, "Expected ')' after expression")
            return expr

        token = self._peek()
        raise SyntaxError(
            f"Expected expression but found '{token.lexeme or token.type.name}'",
            token.line,
            token.column,
        )

    def _match(self, *types: TokenType) -> bool:
        # Si coincide, avanzo.
        for token_type in types:
            if self._check(token_type):
                self._advance()
                return True
        return False

    def _consume(self, token_type: TokenType, message: str) -> Token:
        # Este token tiene que estar sí o sí.
        if self._check(token_type):
            return self._advance()

        token = self._peek()
        raise SyntaxError(message, token.line, token.column)

    def _check(self, token_type: TokenType) -> bool:
        # Solo miro el tipo, sin avanzar.
        if self._is_at_end():
            return False
        return self._peek().type == token_type

    def _advance(self) -> Token:
        # Avanzo al siguiente token.
        if not self._is_at_end():
            self.current += 1
        return self._previous()

    def _is_at_end(self) -> bool:
        # Termina cuando aparece EOF.
        return self._peek().type == TokenType.EOF

    def _peek(self) -> Token:
        # Devuelve el token actual.
        return self.tokens[self.current]

    def _previous(self) -> Token:
        # Devuelve el último token que consumí.
        return self.tokens[self.current - 1]
