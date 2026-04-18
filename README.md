# Analizador / Mini Compilador en Python

## Objetivo del proyecto

Este proyecto implementa un mini compilador en Python. El lenguaje que procesa es chico y permite declarar variables enteras, hacer asignaciones, trabajar con expresiones aritméticas, usar condicionales `if/else` e imprimir valores con `print`.

El programa está dividido en estas partes:

1. **Análisis léxico:** convierte el texto en tokens.
2. **Análisis sintáctico:** revisa la estructura del programa y arma el AST.
3. **Análisis semántico:** comprueba reglas como declaración previa de variables.
4. **Código intermedio:** genera instrucciones de tres direcciones.

La salida de `main.py` muestra la lista de tokens, el AST, la tabla de símbolos y el código intermedio. Si aparece un error, el proceso se detiene en esa parte y muestra la línea y la columna.

## Características principales

- Reconocimiento de palabras reservadas: `int`, `if`, `else`, `print`
- Soporte para identificadores y enteros
- Expresiones aritméticas con `+`, `-`, `*`, `/`
- Comparaciones con `==`, `<`, `>`
- Declaraciones e inicialización de variables
- Asignaciones
- Bloques con `{}`
- Condicionales `if/else`
- Impresión con `print(...)`
- Tabla de símbolos con manejo de ámbitos
- Errores léxicos, sintácticos y semánticos descriptivos
- Generación de código intermedio en tres direcciones

## Estructura del proyecto

- `tokens.py`: define `TokenType` y la clase `Token`.
- `errors.py`: centraliza errores de compilación por fase.
- `lexer.py`: recorre carácter por carácter y construye tokens.
- `parser.py`: implementa un parser LL(1) mediante descenso recursivo.
- `ast_nodes.py`: contiene los nodos del AST y su representación legible.
- `symbol_table.py`: maneja la tabla de símbolos y los ámbitos.
- `semantic_analyzer.py`: aplica reglas semánticas sobre el AST.
- `intermediate_code.py`: genera código de tres direcciones.
- `main.py`: ejecuta todas las fases.
- `examples/`: archivos de prueba válidos y erróneos.

## Gramática utilizada

La gramática se mantuvo simple para poder analizarla con descenso recursivo:

- `program -> statement* EOF`
- `statement -> varDecl | assignment | printStmt | ifStmt | block`
- `varDecl -> 'int' IDENTIFIER '=' expression ';'`
- `assignment -> IDENTIFIER '=' expression ';'`
- `printStmt -> 'print' '(' expression ')' ';'`
- `ifStmt -> 'if' '(' expression ')' statement ('else' statement)?`
- `block -> '{' statement* '}'`
- `expression -> equality`
- `equality -> comparison ( '==' comparison )*`
- `comparison -> term ( ('<' | '>') term )*`
- `term -> factor ( ('+' | '-') factor )*`
- `factor -> primary ( ('*' | '/') primary )*`
- `primary -> INTEGER | IDENTIFIER | '(' expression ')'`

## Cómo ejecutar

Ubicate en la raíz del repositorio y corré:

```bash
python3 main.py examples/valid_program_1.txt
```

También podés probar:

```bash
python3 main.py examples/valid_program_2.txt
python3 main.py examples/lexical_error.txt
python3 main.py examples/syntax_error.txt
python3 main.py examples/semantic_error.txt
```

## Tipos de errores detectados

1. **Errores léxicos:** caracteres no permitidos, por ejemplo `@`.
2. **Errores sintácticos:** estructuras inválidas, como falta de `;` o `)`.
3. **Errores semánticos:** uso de variables no declaradas, redeclaraciones en el mismo bloque o condiciones inválidas.

El resultado es un compilador pequeño, ordenado y fácil de probar desde consola.
