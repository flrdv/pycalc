import enum
import string
from operator import add
from functools import reduce
from abc import ABC, abstractmethod
from typing import List, Iterator, Tuple, Callable, Optional

from pycalc.tokentypes.tokens import Lexeme, Lexemes, Token, Tokens, FuncDef
from pycalc.tokentypes.types import (LexemeType, TokenType, TokenKind,
                                     OPERATORS_TABLE, UNARY_OPERATORS)


class _ParserState(enum.IntEnum):
    ARG = 1
    LAMBDA_ARG = 2
    ARG_COMMA = 3
    LAMBDA_ARG_COMMA = 4
    EQ = 5
    FUNCNAME = 6
    OTHER = 7


class ABCTokenizer(ABC):
    @abstractmethod
    def tokenize(self, data: str) -> Tokens:
        ...


def tokenize(data: str) -> Tokens:
    if not data:
        return []

    tokenizer = Tokenizer()

    return tokenizer.tokenize(data)


class Tokenizer(ABCTokenizer):
    def tokenize(self, data: str) -> Tokens:
        if not data:
            return []

        lexemes: Lexemes = []

        for element, is_op in self._lex(data):
            if is_op:
                op, unaries = self._parse_ops(element)
                lexemes.append(op)
                lexemes.extend(unaries)
            else:
                lexemes.append(self._parse_lexeme(element))

        unary = self._parse_unary(list(map(self._lexeme2token, lexemes)))
        identifiers = self._mark_identifiers(unary)

        return identifiers

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
            if char == " ":
                if buff:
                    yield "".join(buff), state
                    buff.clear()

                continue

            if char in "()":
                if buff:
                    yield "".join(buff), state

                yield char, False
                buff.clear()
            elif (char in operators_chars) + state == 1:
                if buff:
                    yield "".join(buff), state

                buff = [char]
                state = not state
            else:
                buff.append(char)

        if buff:
            yield "".join(buff), state

    def _parse_unary(self, tokens: Tokens) -> Tokens:
        output: Tokens = []
        buffer: Tokens = []

        if tokens[0].kind == TokenKind.OPERATOR:
            buffer.append(tokens[0])
        else:
            output.append(tokens[0])

        for token in tokens[1:]:
            if buffer:
                if token.kind == TokenKind.OPERATOR:
                    buffer.append(token)
                else:
                    output.append(buffer[0])
                    unary = self._calculate_final_unary(buffer[1:])

                    if unary:
                        output.append(Token(
                            kind=TokenKind.UNARY_OPERATOR,
                            typeof=unary,
                            value="+" if unary == TokenType.UN_POS else "-"
                        ))

                    buffer.clear()
                    output.append(token)
            elif token.kind == TokenKind.OPERATOR:
                buffer.append(token)
            else:
                output.append(token)

        if buffer:
            raise SyntaxError("unexpected operator in the end of the expression")

        return output

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

    def _parse_ops(self, raw_op: str) -> Tuple[Lexeme, Lexemes]:
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

            return self._get_op_lexeme(op), list(map(self._get_op_lexeme, raw_op[op_len:]))

        raise SyntaxError("invalid operator: " + raw_op[0])

    @staticmethod
    def _mark_identifiers(tokens: Tokens) -> Tokens:
        """
        Just look for OP_EQ
            - If token in the left:
                - closing brace:
                    - mark everything until opening brace as identifier
                - variable:
                    - mark as IDENTIFIER
                - anything else:
                    - raise exception
        """

        output = []
        state = _ParserState.OTHER
        funcdef = FuncDef("", [])
        eq = Token(
            kind=TokenKind.OPERATOR,
            typeof=TokenType.OP_EQ,
            value="="
        )

        for i, token in enumerate(tokens[::-1]):
            if state == _ParserState.OTHER:
                if token.type == TokenType.OP_EQ:
                    state = _ParserState.EQ
                else:
                    output.append(token)
            elif state == _ParserState.EQ:
                if token.type == TokenType.VAR:
                    token.type = TokenType.IDENTIFIER
                    state = _ParserState.OTHER
                    output.append(eq)
                    output.append(token)
                elif token.type == TokenType.RBRACE:
                    state = _ParserState.ARG
                else:
                    raise SyntaxError(f"cannot assign to {repr(token.value)}")
            elif state == _ParserState.ARG:
                if token.type == TokenType.OP_COMMA:
                    raise SyntaxError("double comma")
                elif token.type == TokenType.LBRACE:
                    state = _ParserState.FUNCNAME
                    continue
                elif token.type != TokenType.VAR:
                    raise SyntaxError(f"disallowed argument identifier: {repr(token.value)}")

                funcdef.args.append(token)
                token.type = TokenType.IDENTIFIER
                state = _ParserState.ARG_COMMA
            elif state == _ParserState.ARG_COMMA:
                if token.type == TokenType.LBRACE:
                    state = _ParserState.FUNCNAME
                elif token.type != TokenType.OP_COMMA:
                    raise SyntaxError(f"expected comma, got {repr(token.value)}")
                else:
                    state = _ParserState.ARG
            elif state == _ParserState.FUNCNAME:
                if token.type not in (TokenType.IDENTIFIER, TokenType.VAR):
                    raise SyntaxError(f"cannot assign func name to {repr(token.value)}")

                funcdef.name = token.value
                funcdef.args.reverse()
                output.append(Token(
                    kind=TokenKind.FUNC,
                    typeof=TokenType.FUNCDEF,
                    value=funcdef
                ))
                funcdef = FuncDef("", [])
                state = _ParserState.OTHER

        if funcdef.name or funcdef.args:
            raise SyntaxError("strange shit happened")

        return output[::-1]

    @staticmethod
    def _get_op_lexeme(op: str) -> Lexeme:
        return Lexeme(
            typeof=LexemeType.OPERATOR,
            value=op
        )

    def _parse_lexeme(self, raw_lexeme: str) -> Lexeme:
        get_lexeme = self._lexeme_getter(raw_lexeme)

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

    @staticmethod
    def _lexeme_getter(value: str) -> Callable[[LexemeType], Lexeme]:
        def getter(typeof: LexemeType) -> Lexeme:
            return Lexeme(
                typeof=typeof,
                value=value
            )

        return getter

    @staticmethod
    def _lexeme2token(lexeme: Lexeme) -> Token:
        braces = {
            LexemeType.LBRACE: TokenType.LBRACE,
            LexemeType.RBRACE: TokenType.RBRACE
        }

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
            if lexeme.value == ":":
                return Token(
                    kind=TokenKind.LITERAL,
                    typeof=TokenType.IDENTIFIER,
                    value=lexeme.value
                )

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
        elif lexeme.type in braces:
            return Token(
                kind=TokenKind.BRACE,
                typeof=braces[lexeme.type],
                value=lexeme.value
            )

        raise SyntaxError("unexpected lexeme type: " + lexeme.type.name)
