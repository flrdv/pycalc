import enum
from string import ascii_letters

UNARY_OPERATORS = {"+", "-"}
ALLOWED_LITERALS = ascii_letters + "_"


class LexemeType(enum.IntEnum):
    UNKNOWN = 0
    NUMBER = 1
    LITERAL = 2
    OPERATOR = 3
    LBRACE = 4
    RBRACE = 5
    DOT = 6
    COMMA = 7


class TokenType(enum.IntEnum):
    NUMBER = 1
    LITERAL = 2
    BRACE_EXPR = 4
    FUNC = 8
    OP_ADD = 16
    OP_SUB = 32
    OP_DIV = 64
    OP_MUL = 128
    OP_POW = 256
    COMMA = 512


OPERATOR = TokenType.OP_ADD | TokenType.OP_SUB | TokenType.OP_DIV | TokenType.OP_MUL | TokenType.OP_POW
OPERATORS_TABLE = {
    "+": TokenType.OP_ADD,
    "-": TokenType.OP_SUB,
    "/": TokenType.OP_DIV,
    "*": TokenType.OP_MUL,
    "^": TokenType.OP_POW
}


class Priorities(enum.IntEnum):
    MINIMAL = 1
    MEDIUM = 2
    HIGH = 3


PRIORITIES_TABLE = {
    TokenType.OP_ADD:   Priorities.MINIMAL,
    TokenType.OP_SUB:   Priorities.MINIMAL,
    TokenType.OP_DIV:   Priorities.MEDIUM,
    TokenType.OP_MUL:   Priorities.MEDIUM,
    TokenType.OP_POW:   Priorities.HIGH,
}
