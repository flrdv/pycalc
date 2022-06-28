from abc import ABC, abstractmethod
from typing import Iterator, List, Tuple

from pycalc.tokentypes.tokens import Token, Tokens, Func, FuncDef
from pycalc.tokentypes.types import (PRIORITIES_TABLE, TokenKind, TokenType,
                                     Stack, InvalidSyntaxError, UnknownTokenError)


class ABCBuilder(ABC):
    @abstractmethod
    def build(self, tokens: List[Tokens]) -> List[Stack[Token]]:
        """
        Builder receives tokens directly from tokenizer. These tokens
        already must be parsed into:
            - Identifiers
            - Variables
            - Unary tokens
            - Function calls and defines
        """


class SortingStationBuilder(ABCBuilder):
    """
    This is a reference implementation of Sorting Station Algorithm
    """

    def build(self, tokens: List[Tokens]) -> List[Stack[Token]]:
        return list(map(self._build_line, tokens))

    def _build_line(self, tokens: Tokens) -> Stack:
        output: Stack[Token] = Stack()
        divider = self._expr_divider(tokens)

        for expr, semicolon_pos in divider:
            stack: Stack[Token] = Stack()
            args_counters = self._count_args(expr)[::-1]

            for i, token in enumerate(expr):
                if token.kind in (TokenKind.NUMBER, TokenKind.STRING)\
                        or token.type == TokenType.IDENTIFIER:
                    output.append(token)
                elif token.type == TokenType.VAR:
                    if i < len(expr)-1 and expr[i+1].type == TokenType.LPAREN:
                        # it's a function!
                        stack.append(self._get_func(token, args_counters.pop()))
                    else:
                        output.append(token)
                elif token.type == TokenType.FUNCDEF:
                    output.append(Token(
                        kind=token.kind,
                        typeof=token.type,
                        value=FuncDef(
                            name=token.value.name,
                            args=token.value.args,
                            body=self._build_line(token.value.body)
                        ),
                        pos=token.pos
                    ))
                elif token.type == TokenType.OP_COMMA:
                    if not stack:
                        raise InvalidSyntaxError(
                            "missing left parenthesis or comma",
                            token.pos
                        )

                    try:
                        while stack.top.type != TokenType.LPAREN:
                            output.append(stack.pop())
                    except IndexError:
                        raise InvalidSyntaxError(
                            "missing left parenthesis or comma",
                            output[-1].pos
                        ) from None
                elif token.kind in (TokenKind.OPERATOR, TokenKind.UNARY_OPERATOR):
                    priority = PRIORITIES_TABLE
                    token_priority = priority[token.type]

                    while stack and (
                        stack.top.kind in (TokenKind.OPERATOR, TokenKind.UNARY_OPERATOR, TokenKind.FUNC)
                        and
                        token_priority <= priority[stack.top.type]
                        and
                        stack.top.type != TokenType.OP_POW
                    ):
                        output.append(stack.pop())

                    stack.append(token)
                elif token.type == TokenType.LPAREN:
                    stack.append(token)
                elif token.type == TokenType.RPAREN:
                    if not stack:
                        raise InvalidSyntaxError(
                            "missing opening parenthesis",
                            token.pos
                        )

                    try:
                        while stack.top.type != TokenType.LPAREN:
                            output.append(stack.pop())
                    except IndexError:
                        raise InvalidSyntaxError(
                            "missing opening parenthesis",
                            output[-1].pos
                        ) from None

                    stack.pop()

                    if stack and stack.top.type == TokenType.FUNCNAME:
                        # it's a function!
                        output.append(self._get_func(stack.pop(), args_counters.pop()))
                else:
                    raise UnknownTokenError(f"unknown token: {token}", token.pos)

            while stack:
                if stack.top.type == TokenType.LPAREN:
                    raise InvalidSyntaxError("missing closing parenthesis", stack.top.pos)

                output.append(stack.pop())

            output.append(Token(
                kind=TokenKind.OPERATOR,
                typeof=TokenType.OP_SEMICOLON,
                value=";",
                pos=semicolon_pos
            ))

        return output[:-1]  # remove trailing semicolon

    def _count_args(self, tokens: Tokens) -> List[int]:
        result = []
        skip_rparens = 0

        for i, token in enumerate(tokens[1:]):
            if skip_rparens:
                if token.type == TokenType.RPAREN:
                    skip_rparens -= 1

                continue

            if token.type == TokenType.LPAREN and tokens[i].type == TokenType.VAR:
                counters = self.__argscounter(tokens[i+2:])
                result.extend(counters)
                skip_rparens = len(counters)

        return result

    def __argscounter(self, tokens: Tokens) -> List[int]:
        result = [0]
        skip_rparens = 0

        waitforcomma = False

        for i, token in enumerate(tokens):
            if skip_rparens:
                if token.type == TokenType.RPAREN:
                    skip_rparens -= 1

                continue
            elif token.type == TokenType.RPAREN:
                return result

            if waitforcomma:
                if token.type == TokenType.OP_COMMA:
                    waitforcomma = False
            elif token.kind != TokenKind.PAREN:
                result[0] += 1
                waitforcomma = True

            if token.type == TokenType.LPAREN:
                counters = self.__argscounter(tokens[i+1:])
                result.extend(counters)
                skip_rparens = len(counters)

        return result

    @staticmethod
    def _expr_divider(expr: Tokens) -> Iterator[Tuple[Tokens, Tuple[int, int]]]:
        """
        Yields expression and semicolon index
        """

        border = 0

        for i, token in enumerate(expr):
            if token.type == TokenType.OP_SEMICOLON:
                yield expr[border:i], token.pos
                border = i + 1

        # semicolon anyway cannot be in the end of the expression,
        # in case it is, error will be raised even before this func
        yield expr[border:], -1

    @staticmethod
    def _get_func(token: Token, argscount: int) -> Token:
        return Token(
            kind=TokenKind.FUNC,
            typeof=TokenType.FUNCCALL,
            value=Func(
                name=token.value,
                argscount=argscount
            ),
            pos=token.pos
        )
