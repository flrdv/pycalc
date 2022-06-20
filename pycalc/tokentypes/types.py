import enum
from string import ascii_letters

UNARY_OPERATORS = {"+", "-"}
ALLOWED_LITERALS = ascii_letters + "_"


class LexemeType(enum.IntEnum):
    UNKNOWN = 0
    NUMBER = 1
    HEXNUMBER = 2
    LITERAL = 3
    OPERATOR = 4
    LBRACE = 5
    RBRACE = 6
    DOT = 7
    COMMA = 8


class TokenKind(enum.IntEnum):
    NUMBER = 0
    LITERAL = 1
    OPERATOR = 2
    UNARY_OPERATOR = 3
    BRACE = 4
    FUNC = 5


class TokenType(enum.IntEnum):
    NUMBER = -1
    OP_EQ = 0
    OP_EQEQ = 1
    OP_NOTEQ = 2
    OP_ADD = 3
    OP_SUB = 4
    OP_DIV = 5
    OP_MUL = 6
    OP_POW = 7
    OP_LSHIFT = 8
    OP_RSHIFT = 9
    OP_BITWISE_AND = 10
    OP_BITWISE_OR = 11
    OP_BITWISE_XOR = 12
    OP_MOD = 13
    OP_FLOORDIV = 14
    OP_SEMICOLON = 15
    OP_COMMA = 16
    UN_POS = 17
    UN_NEG = 18
    LBRACE = 19
    RBRACE = 20
    VAR = 21
    FUNCCALL = 22


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

    TokenType.OP_EQ:        Priorities.NONE,
    TokenType.OP_EQEQ:      Priorities.NONE,
    TokenType.OP_NOTEQ:     Priorities.NONE,
    TokenType.OP_COMMA:     Priorities.NONE,
    TokenType.OP_SEMICOLON: Priorities.NONE,
}
