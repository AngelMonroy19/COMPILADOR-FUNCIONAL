from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Symbol:
    name: str
    var_type: str
    declared_line: int
    declared_column: int
    initialized: bool = False


class SymbolTable:
    def __init__(self) -> None:
        # Empiezo con el ámbito global.
        self.scopes: list[dict[str, Symbol]] = [dict()]
        self.all_symbols: list[Symbol] = []

    def enter_scope(self) -> None:
        # Abro un ámbito nuevo.
        self.scopes.append(dict())

    def exit_scope(self) -> None:
        # Cierro el ámbito actual, salvo que sea el global.
        if len(self.scopes) == 1:
            return
        self.scopes.pop()

    def declare(self, symbol: Symbol) -> None:
        # Guardo el símbolo en el ámbito actual.
        current_scope = self.scopes[-1]
        current_scope[symbol.name] = symbol
        self.all_symbols.append(symbol)

    def declared_in_current_scope(self, name: str) -> bool:
        # Me sirve para ver si ya existe en este bloque.
        return name in self.scopes[-1]

    def resolve(self, name: str) -> Symbol | None:
        # Busco desde el ámbito más interno hacia afuera.
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None

    def flatten(self) -> list[Symbol]:
        # Devuelvo todo junto para imprimirlo.
        return list(self.all_symbols)
