import enum
from abc import ABC, abstractmethod
from typing import Optional, List

from pycalc.tokentypes.tokens import Token, Tokens, Lexeme, Lexemes, FuncCall
from pycalc.tokentypes.types import (LexemeType, TokenType, TokenKind, UNARY_OPERATORS,
                                     OPERATORS_TABLE)


class ABCParser(ABC):
    @abstractmethod
    def parse(self, lexemes: Lexemes) -> Tokens:
        ...


class _UnaryParseState(enum.IntEnum):
    operator = 1
    unary = 2
    token = 3


class Parser(ABCParser):
    def parse(self, lexemes: Lexemes) -> Tokens:
        if not lexemes:
            return []

        tokens = self._parse_braces(lexemes)
        unary = self._parse_unary(tokens)
        # funcs = self._parse_functions(unary)

        return unary

    def _parse_braces(self, lexemes: Lexemes) -> Tokens:
        result: Tokens = []
        buff: Lexemes = []
        opened_braces = 0

        for lexeme in lexemes:
            if buff:
                if lexeme.type == LexemeType.LBRACE:
                    opened_braces += 1
                elif lexeme.type == LexemeType.RBRACE:
                    if opened_braces:
                        opened_braces -= 1
                    else:
                        result.append(Token(
                            kind=TokenKind.BRACE_EXPR,
                            typeof=TokenType.BRACE_EXPR,
                            value=self._parse_braces(buff[1:])
                        ))
                        buff.clear()
                        continue

                buff.append(lexeme)
            else:
                if lexeme.type == LexemeType.LBRACE:
                    buff.append(lexeme)
                    continue

                result.append(_lexeme2token(lexeme))

        if buff or opened_braces:
            raise SyntaxError("unclosed brace")

        return result

    def _parse_unary(self, tokens: Tokens) -> Tokens:
        result: Tokens = []
        buff: Tokens = []

        if tokens[0].kind == TokenKind.OPERATOR:
            state = _UnaryParseState.unary
        else:
            state = _UnaryParseState.token

        for token in tokens:
            if token.kind == TokenKind.BRACE_EXPR:
                token.value = self._parse_unary(token.value)

            if state == _UnaryParseState.operator:
                if token.kind != TokenKind.OPERATOR:
                    raise SyntaxError("invalid expression")

                result.append(token)
                state = _UnaryParseState.unary
            elif state == _UnaryParseState.unary:
                if token.kind != TokenKind.OPERATOR:
                    if buff:
                        unary = self._calculate_final_unary(buff)
                        result.append(Token(
                            kind=TokenKind.UNARY_OPERATOR,
                            typeof=unary,
                            value="+" if unary == TokenType.UN_POS else "-"
                        ))
                        buff.clear()

                    result.append(token)
                    state = _UnaryParseState.token
                else:
                    buff.append(token)
            elif state == _UnaryParseState.token:
                result.append(token)
                state = _UnaryParseState.operator

        if buff or state == _UnaryParseState.unary:
            raise SyntaxError("incomplete expression")

        return result

    @staticmethod
    def _calculate_final_unary(ops: Tokens) -> Optional[TokenType]:
        if not ops:
            return None

        subs = 0

        for token in ops:
            if token.value not in UNARY_OPERATORS:
                raise SyntaxError(f"disallowed unary: {token.value}")

            subs += token.value == '-'

        # hehe, pretty tricky, isn't it?
        return TokenType.UN_NEG if subs & 1 else TokenType.UN_POS


def _lexeme2token(lexeme: Lexeme) -> Token:
    if lexeme.type == LexemeType.NUMBER:
        return Token(
            kind=TokenKind.NUMBER,
            typeof=TokenType.NUMBER,
            value=float(lexeme.value)
        )
    elif lexeme.type == LexemeType.HEXNUMBER:
        return Token(
            kind=TokenKind.NUMBER,
            typeof=TokenType.NUMBER,
            value=int(lexeme.value[2:], 16)
        )
    elif lexeme.type == LexemeType.LITERAL:
        return Token(
            kind=TokenKind.LITERAL,
            typeof=TokenType.VAR,
            value=lexeme.value
        )
    elif lexeme.type == LexemeType.OPERATOR:
        return Token(
            kind=TokenKind.OPERATOR,
            typeof=OPERATORS_TABLE[lexeme.value],
            value=lexeme.value
        )

    raise SyntaxError("unexpected lexeme type: " + lexeme.type.name)
