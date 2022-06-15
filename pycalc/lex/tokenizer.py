import string
from operator import add
from functools import reduce
from abc import ABC, abstractmethod
from typing import List, Iterator, Tuple, Callable

from pycalc.tokentypes.tokens import Lexeme, Lexemes
from pycalc.tokentypes.types import LexemeType, OPERATORS_TABLE


class ABCTokenizer(ABC):
    @abstractmethod
    def tokenize(self, data: str) -> Lexemes:
        ...


def tokenize(data: str) -> Lexemes:
    if not data:
        return []

    tokenizer = Tokenizer()

    return tokenizer.tokenize(data)


class Tokenizer(ABCTokenizer):
    @staticmethod
    def _lex(data: str) -> Iterator[Tuple[str, bool]]:
        buff: List[str] = [data[0]]
        operators_chars = set(reduce(add, OPERATORS_TABLE.keys()))

        if data[0] == "(":
            yield "(", False
            buff.clear()
            state = False
        else:
            # True is operator, False is not operator
            state = data[0] in operators_chars

        for char in data[1:]:
            if char in "()":
                if buff:
                    yield "".join(buff), state

                yield char, False
                buff = []
            elif (char in operators_chars) + state == 1:
                if buff:
                    yield "".join(buff), state

                buff = [char]
                state = not state
            else:
                buff.append(char)

        if buff:
            yield "".join(buff), state

    def tokenize(self, data: str) -> Lexemes:
        if not data:
            return []

        lexemes: Lexemes = []

        for element, is_op in self._lex(data):
            if is_op:
                op, unaries = _parse_op(element)
                lexemes.append(op)
                lexemes.extend(unaries)
            else:
                lexemes.append(_parse_lexeme(element))

        return lexemes


def _parse_op(raw_op: str) -> Tuple[Lexeme, Lexemes]:
    """
    Splits a string of operators into actual and
    unary operators
    """

    op_len = len(max(OPERATORS_TABLE.keys(), key=len))

    while op_len > 0:
        op = raw_op[:op_len]

        if op not in OPERATORS_TABLE:
            op_len -= 1
            continue

        return _get_op_lexeme(op), list(map(_get_op_lexeme, raw_op[op_len:]))

    raise SyntaxError("invalid operator: " + raw_op[0])


def _get_op_lexeme(op: str) -> Lexeme:
    return Lexeme(
        typeof=LexemeType.OPERATOR,
        value=op
    )


def _parse_lexeme(raw_lexeme: str) -> Lexeme:
    get_lexeme = _lexeme_getter(raw_lexeme)

    if raw_lexeme.startswith("0x"):
        if len(raw_lexeme) == 2:
            raise SyntaxError("invalid hexdecimal value: 0x")

        return get_lexeme(LexemeType.HEXNUMBER)
    elif raw_lexeme[0] in string.digits + ".":
        if len(raw_lexeme) == raw_lexeme.count("."):
            raise SyntaxError("invalid float: " + raw_lexeme)

        return get_lexeme(LexemeType.NUMBER)
    elif raw_lexeme == "(":
        return get_lexeme(LexemeType.LBRACE)
    elif raw_lexeme == ")":
        return get_lexeme(LexemeType.RBRACE)

    return get_lexeme(LexemeType.LITERAL)


def _lexeme_getter(value: str) -> Callable[[LexemeType], Lexeme]:
    def getter(typeof: LexemeType) -> Lexeme:
        return Lexeme(
            typeof=typeof,
            value=value
        )

    return getter
