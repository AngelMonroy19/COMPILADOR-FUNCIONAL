from __future__ import annotations

from errors import LexicalError
from tokens import Token, TokenType


class Lexer:
    RESERVED_WORDS = {
        "int": TokenType.INT,
        "if": TokenType.IF,
        "else": TokenType.ELSE,
        "print": TokenType.PRINT,
    }

    SINGLE_CHAR_TOKENS = {
        "+": TokenType.PLUS,
        "-": TokenType.MINUS,
        "*": TokenType.STAR,
        "/": TokenType.SLASH,
        "=": TokenType.ASSIGN,
        "<": TokenType.LESS,
        ">": TokenType.GREATER,
        ";": TokenType.SEMICOLON,
        "{": TokenType.LBRACE,
        "}": TokenType.RBRACE,
        "(": TokenType.LPAREN,
        ")": TokenType.RPAREN,
    }

    def __init__(self, source: str) -> None:
        # Guardo el texto y dejo listos los punteros del recorrido.
        self.source = source
        self.tokens: list[Token] = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.column = 1
        self.start_line = 1
        self.start_column = 1

    def scan_tokens(self) -> list[Token]:
        # Recorro todo el fuente y voy armando la lista de tokens.
        while not self._is_at_end():
            self.start = self.current
            self.start_line = self.line
            self.start_column = self.column
            self._scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line, self.column))
        return self.tokens

    def _scan_token(self) -> None:
        # Miro el carácter actual y decido qué hacer con él.
        char = self._advance()

        if char in (" ", "\r", "\t"):
            return
        if char == "\n":
            return

        if char == "=" and self._match("="):
            self._add_token(TokenType.EQUAL_EQUAL)
            return

        if char in self.SINGLE_CHAR_TOKENS:
            self._add_token(self.SINGLE_CHAR_TOKENS[char])
            return

        if char.isdigit():
            self._number()
            return

        if char.isalpha() or char == "_":
            self._identifier_or_keyword()
            return

        raise LexicalError(f"Unexpected character '{char}'", self.start_line, self.start_column)

    def _identifier_or_keyword(self) -> None:
        # Acá junto letras y números para formar nombres.
        while self._peek().isalnum() or self._peek() == "_":
            self._advance()

        lexeme = self.source[self.start : self.current]
        token_type = self.RESERVED_WORDS.get(lexeme, TokenType.IDENTIFIER)
        self.tokens.append(Token(token_type, lexeme, None, self.start_line, self.start_column))

    def _number(self) -> None:
        # Acá junto todos los dígitos del número.
        while self._peek().isdigit():
            self._advance()

        lexeme = self.source[self.start : self.current]
        self.tokens.append(
            Token(TokenType.INTEGER, lexeme, int(lexeme), self.start_line, self.start_column)
        )

    def _add_token(self, token_type: TokenType) -> None:
        # Este caso es para tokens simples como ; o +.
        lexeme = self.source[self.start : self.current]
        self.tokens.append(Token(token_type, lexeme, None, self.start_line, self.start_column))

    def _is_at_end(self) -> bool:
        # Me dice si ya llegué al final.
        return self.current >= len(self.source)

    def _advance(self) -> str:
        # Avanzo un carácter y actualizo la posición.
        char = self.source[self.current]
        self.current += 1
        if char == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char

    def _peek(self) -> str:
        # Miro el siguiente carácter sin gastarlo.
        if self._is_at_end():
            return "\0"
        return self.source[self.current]

    def _match(self, expected: str) -> bool:
        # Lo uso cuando necesito ver si viene un segundo símbolo, como en ==.
        if self._is_at_end() or self.source[self.current] != expected:
            return False
        self._advance()
        return True
