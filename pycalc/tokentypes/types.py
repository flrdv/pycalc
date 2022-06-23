import enum
from string import ascii_letters
from typing import Union, Dict, Callable


Number = Union[int, float]
NamespaceValue = Union[Number, Callable]
Namespace = Dict[str, NamespaceValue]

UNARY_OPERATORS = {"+", "-"}
ALLOWED_LITERALS = ascii_letters + "_"


class Stack(list):
    @property
    def top(self):
        return self[-1]


class LexemeType(enum.IntEnum):
    UNKNOWN = 0
    NUMBER = 1
    HEXNUMBER = 2
    FLOAT = 3
    LITERAL = 4
    OPERATOR = 5
    LBRACE = 6
    RBRACE = 7
    DOT = 8
    COMMA = 9


class TokenKind(enum.IntEnum):
    NUMBER = 0
    LITERAL = 1
    OPERATOR = 2
    UNARY_OPERATOR = 3
    BRACE = 4
    FUNC = 5
    OTHER = 6


class TokenType(enum.IntEnum):
    FLOAT = 0
    INTEGER = 1
    OP_EQ = 2
    OP_EQEQ = 3
    OP_NOTEQ = 4
    OP_ADD = 5
    OP_SUB = 6
    OP_DIV = 7
    OP_MUL = 8
    OP_POW = 9
    OP_LSHIFT = 10
    OP_RSHIFT = 11
    OP_BITWISE_AND = 12
    OP_BITWISE_OR = 13
    OP_BITWISE_XOR = 14
    OP_MOD = 15
    OP_FLOORDIV = 16
    OP_SEMICOLON = 17
    OP_COMMA = 18
    UN_POS = 19
    UN_NEG = 20
    LBRACE = 21
    RBRACE = 22
    VAR = 23
    IDENTIFIER = 24
    FUNCCALL = 25
    FUNCDEF = 26
    FUNCNAME = 27
    OTHER = 28


OPERATORS_TABLE = {
    "+": TokenType.OP_ADD,
    "-": TokenType.OP_SUB,
    "/": TokenType.OP_DIV,
    "//": TokenType.OP_FLOORDIV,
    "*": TokenType.OP_MUL,
    "**": TokenType.OP_POW,
    "%": TokenType.OP_MOD,
    "<<": TokenType.OP_LSHIFT,
    ">>": TokenType.OP_RSHIFT,
    "&": TokenType.OP_BITWISE_AND,
    "|": TokenType.OP_BITWISE_OR,
    "^": TokenType.OP_BITWISE_XOR,

    "==": TokenType.OP_EQEQ,
    "!=": TokenType.OP_NOTEQ,

    ";": TokenType.OP_SEMICOLON,
    "=": TokenType.OP_EQ,
    ",": TokenType.OP_COMMA
}


class Priorities(enum.IntEnum):
    NONE = 0
    MINIMAL = 1
    MEDIUM = 2
    HIGH = 3
    MAXIMAL = 4


PRIORITIES_TABLE = {
    TokenType.OP_ADD:      Priorities.MINIMAL,
    TokenType.OP_SUB:      Priorities.MINIMAL,

    TokenType.OP_DIV:         Priorities.MEDIUM,
    TokenType.OP_FLOORDIV:    Priorities.MEDIUM,
    TokenType.OP_MUL:         Priorities.MEDIUM,
    TokenType.OP_MOD:         Priorities.MEDIUM,
    TokenType.OP_LSHIFT:      Priorities.MEDIUM,
    TokenType.OP_RSHIFT:      Priorities.MEDIUM,
    TokenType.OP_BITWISE_AND: Priorities.MEDIUM,
    TokenType.OP_BITWISE_OR:  Priorities.MEDIUM,
    TokenType.OP_BITWISE_XOR: Priorities.MEDIUM,

    TokenType.UN_POS: Priorities.HIGH,
    TokenType.UN_NEG: Priorities.HIGH,

    TokenType.OP_POW:   Priorities.MAXIMAL,
    TokenType.FUNCCALL: Priorities.MAXIMAL,
    TokenType.FUNCDEF:  Priorities.MAXIMAL,

    TokenType.OP_EQ:        Priorities.NONE,
    TokenType.OP_EQEQ:      Priorities.NONE,
    TokenType.OP_NOTEQ:     Priorities.NONE,
    TokenType.OP_COMMA:     Priorities.NONE,
    TokenType.OP_SEMICOLON: Priorities.NONE,
}


class PyCalcError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class InvalidSyntaxError(PyCalcError):
    pass


class ArgumentsError(PyCalcError):
    pass


class NameNotFoundError(PyCalcError):
    pass
