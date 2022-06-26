import enum
import string
from operator import add
from functools import reduce
from abc import ABC, abstractmethod
from typing import List, Iterator, Tuple, Callable

from pycalc.tokentypes.tokens import Lexeme, Lexemes, Token, Tokens, FuncDef
from pycalc.tokentypes.types import (LexemeType, TokenType, TokenKind,
                                     OPERATORS_TABLE, UNARY_OPERATORS,
                                     Stack, InvalidSyntaxError)


class _ParserState(enum.IntEnum):
    ARG = 1
    ARG_COMMA = 3
    EQ = 5
    FUNCNAME = 6
    OTHER = 7


class ABCTokenizer(ABC):
    @abstractmethod
    def tokenize(self, data: str) -> Tokens:
        """
        Tokenizer is 2 in 1: lexer+parser. Lexer is just a generator
        that yields lexemes (strings that are single language piece).
        Parser parses unary, marks identifiers (for example, variable
        names), function calls (counts arguments function call provides)
        and function defines (creates FuncDef token with all the args
        and name function takes; also OP_EQ is ignored in this case)
        """


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

        for element, is_op, pos in self._lex(data):
            if is_op:
                op, unaries = self._parse_ops(element, pos)
                lexemes.append(op)
                lexemes.extend(unaries)
            else:
                lexemes.append(self._parse_lexeme(element, pos))

        unary = self._parse_unary(list(map(
            self._lexeme2token, lexemes
        )))
        identifiers = self._mark_identifiers(unary)

        return identifiers

    @staticmethod
    def _lex(data: str) -> Iterator[Tuple[str, bool, int]]:
        buff: List[str] = [data[0]]
        operators_chars = set(reduce(add, OPERATORS_TABLE.keys()))

        if data[0] == "(":
            yield "(", False, 0
            buff.clear()
            state = False
        else:
            # True is operator, False is not operator
            state = data[0] in operators_chars

        for i, char in enumerate(data[1:], start=1):
            if char == " ":
                if buff:
                    yield "".join(buff), state, i-len(buff)
                    buff.clear()

                continue

            if char in "()":
                if buff:
                    yield "".join(buff), state, i-len(buff)

                yield char, False, i
                buff.clear()
            elif (char in operators_chars) + state == 1:
                if buff:
                    yield "".join(buff), state, i-len(buff)

                buff = [char]
                state = not state
            else:
                buff.append(char)

        if buff:
            yield "".join(buff), state, len(data)-len(buff)

    def _parse_unary(self, tokens: Tokens) -> Tokens:
        output: Tokens = []
        buffer: Tokens = []
        i = -1

        if tokens[0].kind == TokenKind.OPERATOR:
            for i, token in enumerate(tokens):
                if token.kind != TokenKind.OPERATOR:
                    tokens = tokens[i:]
                    break

                buffer.append(token)

            unary = self._calculate_final_unary(buffer, i)
            output.append(Token(
                kind=TokenKind.UNARY_OPERATOR,
                typeof=unary,
                value="+" if unary == TokenType.UN_POS else "-",
                pos=0
            ))
            buffer.clear()
        else:
            output.append(tokens[0])
            tokens = tokens[1:]

        for i, token in enumerate(tokens):
            if buffer:
                if token.kind == TokenKind.OPERATOR:
                    buffer.append(token)
                else:
                    output.append(buffer[0])

                    if buffer[1:]:
                        unary = self._calculate_final_unary(buffer[1:], i-len(buffer)+1)
                        output.append(Token(
                            kind=TokenKind.UNARY_OPERATOR,
                            typeof=unary,
                            value="+" if unary == TokenType.UN_POS else "-",
                            pos=len(output)-1
                        ))

                    buffer.clear()
                    output.append(token)
            elif token.kind == TokenKind.OPERATOR:
                buffer.append(token)
            else:
                output.append(token)

        if buffer:
            raise InvalidSyntaxError("unexpected operator in the end of the expression", buffer[-1].pos)

        return output

    @staticmethod
    def _calculate_final_unary(ops: Tokens, pos: int) -> TokenType:
        if not ops:
            raise ValueError("_calculate_final_query(): ops are empty")

        subs = 0

        for i, token in enumerate(ops):
            if token.value not in UNARY_OPERATORS:
                raise InvalidSyntaxError(f"illegal unary: {token.value}", pos+i+1)

            subs += token.value == '-'

        # hehe, pretty tricky, isn't it?
        return TokenType.UN_NEG if subs & 1 else TokenType.UN_POS

    def _parse_ops(self, raw_op: str, pos: int) -> Tuple[Lexeme, Lexemes]:
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

            oper = self._get_op_lexeme(op, pos)
            unaries = map(
                lambda op_: self._get_op_lexeme(op_, pos+op_len),
                raw_op[op_len:]
            )

            return oper, list(unaries)

        raise InvalidSyntaxError("illegal operator: " + raw_op[0], pos)

    def _mark_identifiers(self, tokens: Tokens) -> Tokens:
        output = []
        state = _ParserState.OTHER
        empty_stack = Stack()
        funcdef = FuncDef("", [], empty_stack)
        prev_eq_pos = None

        for i, token in enumerate(tokens[::-1]):
            if state == _ParserState.OTHER:
                if token.type == TokenType.OP_EQ:
                    state = _ParserState.EQ
                    prev_eq_pos = token.pos
                else:
                    output.append(token)
            elif state == _ParserState.EQ:
                if token.type == TokenType.VAR:
                    token.type = TokenType.IDENTIFIER
                    state = _ParserState.OTHER
                    output.append(Token(
                        kind=TokenKind.OPERATOR,
                        typeof=TokenType.OP_EQ,
                        value="=",
                        pos=prev_eq_pos,
                    ))
                    output.append(token)
                elif token.type == TokenType.RPAREN:
                    state = _ParserState.ARG
                else:
                    raise InvalidSyntaxError(f"cannot assign to {repr(token.value)}", len(tokens)-i-1)
            elif state == _ParserState.ARG:
                if token.type == TokenType.OP_COMMA:
                    raise InvalidSyntaxError("double comma", len(tokens)-i-1)
                elif token.type == TokenType.LPAREN:
                    state = _ParserState.FUNCNAME
                    continue
                elif token.type != TokenType.VAR:
                    raise InvalidSyntaxError(
                        f"illegal argument identifier: {repr(token.value)}",
                        token.pos
                    )

                funcdef.args.append(token)
                token.type = TokenType.IDENTIFIER
                state = _ParserState.ARG_COMMA
            elif state == _ParserState.ARG_COMMA:
                if token.type == TokenType.LPAREN:
                    state = _ParserState.FUNCNAME
                elif token.type != TokenType.OP_COMMA:
                    raise InvalidSyntaxError(
                        f"expected comma, got {repr(token.value)}",
                        len(tokens)-i
                    )
                else:
                    state = _ParserState.ARG
            elif state == _ParserState.FUNCNAME:
                if token.type not in (TokenType.IDENTIFIER, TokenType.VAR):
                    funcdef.name = ""

                    if token.type == TokenType.OP_EQ:
                        state = _ParserState.EQ
                    else:
                        state = _ParserState.OTHER
                else:
                    funcdef.name = token.value
                    state = _ParserState.OTHER

                funcdef.args.reverse()
                output.append(Token(
                    kind=TokenKind.FUNC,
                    typeof=TokenType.FUNCDEF,
                    value=funcdef,
                    pos=len(tokens)-i-1
                ))

                if token.type not in (TokenType.IDENTIFIER, TokenType.VAR, TokenType.OP_EQ):
                    output.append(token)

                funcdef = FuncDef("", [], empty_stack)

        if funcdef.name or funcdef.args:
            raise InvalidSyntaxError("strange shit happened", len(tokens)-1)

        return self._fill_funcbodies(output[::-1])

    def _fill_funcbodies(self, tokens: Tokens) -> Tokens:
        output: Tokens = []
        bodybuff = []
        lparens = 0

        for token in tokens:
            if bodybuff:
                if token.type == TokenType.LPAREN:
                    lparens += 1
                    bodybuff.append(token)
                elif lparens and token.type == TokenType.RPAREN:
                    lparens -= 1
                    bodybuff.append(token)
                elif not lparens and token.type in (TokenType.OP_COMMA, TokenType.RPAREN):
                    bodybuff[0].value.body = self._fill_funcbodies(bodybuff[1:])
                    output.append(bodybuff[0])
                    output.append(token)
                    bodybuff.clear()
                else:
                    bodybuff.append(token)
            else:
                if token.type == TokenType.FUNCDEF:
                    bodybuff.append(token)
                else:
                    output.append(token)

        if bodybuff:
            bodybuff[0].value.body = self._fill_funcbodies(bodybuff[1:])
            output.append(bodybuff[0])

        return output

    @staticmethod
    def _get_op_lexeme(op: str, pos: int) -> Lexeme:
        return Lexeme(
            typeof=LexemeType.OPERATOR,
            value=op,
            pos=pos
        )

    def _parse_lexeme(self, raw_lexeme: str, pos: int) -> Lexeme:
        get_lexeme = self._lexeme_getter(raw_lexeme, pos)

        if raw_lexeme.startswith("0x"):
            if len(raw_lexeme) == 2:
                raise InvalidSyntaxError("invalid hexdecimal value: 0x", pos)

            return get_lexeme(LexemeType.HEXNUMBER)
        elif raw_lexeme[0] in string.digits + ".":
            if len(raw_lexeme) == raw_lexeme.count(".") or raw_lexeme.count(".") > 1:
                raise InvalidSyntaxError("invalid float: " + raw_lexeme, pos)

            if "." in raw_lexeme:
                return get_lexeme(LexemeType.FLOAT)

            return get_lexeme(LexemeType.NUMBER)
        elif raw_lexeme == "(":
            return get_lexeme(LexemeType.LPAREN)
        elif raw_lexeme == ")":
            return get_lexeme(LexemeType.RPAREN)

        return get_lexeme(LexemeType.LITERAL)

    @staticmethod
    def _lexeme_getter(value: str, pos: int) -> Callable[[LexemeType], Lexeme]:
        def getter(typeof: LexemeType) -> Lexeme:
            return Lexeme(
                typeof=typeof,
                value=value,
                pos=pos
            )

        return getter

    @staticmethod
    def _lexeme2token(lexeme: Lexeme) -> Token:
        parentheses = {
            LexemeType.LPAREN: TokenType.LPAREN,
            LexemeType.RPAREN: TokenType.RPAREN
        }

        if lexeme.type == LexemeType.NUMBER:
            return Token(
                kind=TokenKind.NUMBER,
                typeof=TokenType.INTEGER,
                value=int(lexeme.value),
                pos=lexeme.pos
            )
        elif lexeme.type == LexemeType.FLOAT:
            return Token(
                kind=TokenKind.NUMBER,
                typeof=TokenType.FLOAT,
                value=float(lexeme.value),
                pos=lexeme.pos
            )
        elif lexeme.type == LexemeType.HEXNUMBER:
            return Token(
                kind=TokenKind.NUMBER,
                typeof=TokenType.INTEGER,
                value=int(lexeme.value[2:], 16),
                pos=lexeme.pos
            )
        elif lexeme.type == LexemeType.LITERAL:
            return Token(
                kind=TokenKind.LITERAL,
                typeof=TokenType.VAR,
                value=lexeme.value,
                pos=lexeme.pos
            )
        elif lexeme.type == LexemeType.OPERATOR:
            return Token(
                kind=TokenKind.OPERATOR,
                typeof=OPERATORS_TABLE[lexeme.value],
                value=lexeme.value,
                pos=lexeme.pos
            )
        elif lexeme.type in parentheses:
            return Token(
                kind=TokenKind.PAREN,
                typeof=parentheses[lexeme.type],
                value=lexeme.value,
                pos=lexeme.pos
            )

        raise InvalidSyntaxError("unexpected lexeme type: " + lexeme.type.name, lexeme.pos)
