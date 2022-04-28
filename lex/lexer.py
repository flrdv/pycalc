from abc import ABC, abstractmethod
from typing import List

from tokentypes.tokens import Lexeme, Lexemes
from tokentypes.types import LexemeType, OPERATORS_TABLE, ALLOWED_LITERALS


class ABCLexer(ABC):
    @abstractmethod
    def lex(self, data: str) -> Lexemes:
        ...


def lex(data: str) -> Lexemes:
    if not data:
        return []

    lexer = Lexer()

    return lexer.lex(data)


class Lexer(ABCLexer):
    """
    Lexer is a finite-state machine that parses an input stream.

    Warning: this is not a universal lexer, it does not allow everything, that is not
    an operator (listed in tokentypes.types.OPERATORS), a literal (listed in
    tokentypes.types.ALLOWED_LITERALS), and is not a number (integer or float)
    """

    LEXER_SAME_TOKENS_EXCEPTIONS = (LexemeType.OPERATOR, LexemeType.LBRACE, LexemeType.RBRACE)

    def __init__(self):
        self.state: LexemeType = LexemeType.UNKNOWN
        self.tempbuf: List[str] = []

    def lex(self, data: str) -> Lexemes:
        lexemes: Lexemes = []

        if not data:
            return []

        self.state = get_char_type(data[0])
        self.tempbuf.append(data[0])

        for char in data[1:]:
            if not char.strip():
                # skip whitespaces, newlines, tabs, etc.
                continue

            typeofchar = get_char_type(char)

            if typeofchar != self.state or typeofchar in self.LEXER_SAME_TOKENS_EXCEPTIONS:
                if not (self.state == LexemeType.LITERAL and typeofchar == LexemeType.NUMBER) and \
                        not (self.state == LexemeType.NUMBER and typeofchar == LexemeType.DOT):
                    lexemes.append(Lexeme(
                        typeof=self.state,
                        value="".join(self.tempbuf)
                    ))
                    self.state = typeofchar
                    self.tempbuf.clear()

            self.tempbuf.append(char)

        lexemes.append(Lexeme(
            typeof=self.state,
            value="".join(self.tempbuf)
        ))

        self.state = LexemeType.UNKNOWN
        self.tempbuf.clear()

        return lexemes


def get_char_type(char: str) -> LexemeType:
    if char == '(':
        return LexemeType.LBRACE
    elif char == ')':
        return LexemeType.RBRACE
    elif char == '.':
        return LexemeType.DOT
    elif char == ',':
        return LexemeType.COMMA
    elif _is_number(char):
        return LexemeType.NUMBER
    elif char in OPERATORS_TABLE:
        return LexemeType.OPERATOR
    elif char in ALLOWED_LITERALS:
        return LexemeType.LITERAL

    raise TypeError("disallowed char: " + char)


def _is_number(string: str) -> int:
    """
    Why not string.isdigit()? Because .isdigit() may return True even in case
    int(string) will raise ValueError
    """

    try:
        float(string)
        return True
    except ValueError:
        return False
