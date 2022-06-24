from typing import List, Union, Callable

from . import types

Lexemes = List["Lexeme"]
Tokens = List["Token"]
TokenValue = Union[int, float, str, "Func", "FuncDef"]


class Lexeme:
    """
    A class that contains a raw piece of input stream.
    It may be: number, literal, operator, lbrace, rbrace
    """

    def __init__(self, typeof: types.LexemeType, value: str):
        self.type = typeof
        self.value = value

    def __str__(self):
        return f"Lexeme(type={self.type.name}, value={repr(self.value)})"

    __repr__ = __str__


class Token:
    def __init__(self,
                 kind: types.TokenKind,
                 typeof: types.TokenType,
                 value: TokenValue,
                 ):
        self.kind = kind
        self.type = typeof
        self.value = value

    def __str__(self):
        return f"Token(kind={self.kind.name}, type={self.type.name}, value={repr(self.value)})"

    __repr__ = __str__


class Func:
    """
    Func just represents some information about function call
    """

    def __init__(self, name: str, argscount: int):
        self.name = name
        self.argscount = argscount

    def __str__(self):
        return f"Func(name={repr(self.name)}, argscount={self.argscount})"

    __repr__ = __str__


class FuncDef:
    """
    FuncDef represents function defining
    """

    def __init__(self, name: str, args: Tokens):
        self.name = name
        self.args = args

    def __str__(self):
        return f"FuncDef(name={repr(self.name)}, args=({','.join(arg.value for arg in self.args)}))"

    __repr__ = __str__


class Function:
    def __init__(self, name: str, target: Callable):
        self.name = name
        self.target = target

    @property
    def __call__(self):
        return self.target

    def __str__(self):
        return self.name

    __repr__ = __str__
