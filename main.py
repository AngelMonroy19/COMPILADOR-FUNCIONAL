from __future__ import annotations

import sys

from errors import CompilerError, LexicalError, SemanticError, SyntaxError
from intermediate_code import IntermediateCodeGenerator
from lexer import Lexer
from parser import Parser
from semantic_analyzer import SemanticAnalyzer


def print_tokens(tokens) -> None:
    # Muestro los tokens y salto el EOF para no ensuciar la salida.
    print("=== TOKENS ===")
    for token in tokens:
        if token.type.name == "EOF":
            continue
        print(token)


def print_ast(program) -> None:
    # Imprime el árbol en un formato fácil de leer.
    print("\n=== AST ===")
    print(program.pretty())


def print_symbol_table(symbol_table) -> None:
    # Acá se ve qué variables quedaron registradas.
    print("\n=== TABLA DE SÍMBOLOS ===")
    symbols = symbol_table.flatten()
    if not symbols:
        print("(vacía)")
        return
    for symbol in symbols:
        print(
            f"name={symbol.name}, type={symbol.var_type}, "
            f"declared_at={symbol.declared_line}:{symbol.declared_column}, "
            f"initialized={symbol.initialized}"
        )


def print_intermediate_code(instructions: list[str]) -> None:
    # Numero las instrucciones para seguir mejor el orden.
    print("\n=== CÓDIGO INTERMEDIO ===")
    if not instructions:
        print("(vacío)")
        return
    for index, instruction in enumerate(instructions, start=1):
        print(f"{index:03d}: {instruction}")


def run_compiler(source_code: str) -> None:
    # Primero saco los tokens.
    lexer = Lexer(source_code)
    tokens = lexer.scan_tokens()
    print_tokens(tokens)

    # Después armo el AST.
    parser = Parser(tokens)
    program = parser.parse()
    print_ast(program)

    # Luego reviso semántica y tabla de símbolos.
    semantic_analyzer = SemanticAnalyzer()
    symbol_table = semantic_analyzer.analyze(program)
    print_symbol_table(symbol_table)

    # Al final genero el código intermedio.
    code_generator = IntermediateCodeGenerator()
    instructions = code_generator.generate(program)
    print_intermediate_code(instructions)


def main() -> int:
    # Espero un solo archivo por parámetro.
    if len(sys.argv) != 2:
        print("Uso: python3 main.py <archivo_fuente>")
        return 1

    source_path = sys.argv[1]
    try:
        # Leo todo el archivo de entrada.
        with open(source_path, "r", encoding="utf-8") as file:
            source_code = file.read()
    except OSError as error:
        print(f"Error al leer '{source_path}': {error}")
        return 1

    try:
        # Corro todas las fases del compilador.
        run_compiler(source_code)
        return 0
    except LexicalError as error:
        print(f"\n[STOP] {error}")
        return 1
    except SyntaxError as error:
        print(f"\n[STOP] {error}")
        return 1
    except SemanticError as error:
        print(f"\n[STOP] {error}")
        return 1
    except CompilerError as error:
        print(f"\n[STOP] Error del compilador: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
