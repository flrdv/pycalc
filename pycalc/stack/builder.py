from abc import ABC, abstractmethod
from typing import Iterator, List

from pycalc.tokentypes.tokens import Token, Tokens, Func
from pycalc.tokentypes.types import PRIORITIES_TABLE, TokenKind, TokenType


class Stack(list):
    @property
    def top(self):
        return self[-1]


class ABCBuilder(ABC):
    @abstractmethod
    def build(self, tokens: Tokens) -> Stack:
        ...


class SortingStationBuilder(ABCBuilder):
    """
    This is a reference implementation of Sorting Station Algorithm
    """

    def build(self, tokens: Tokens) -> Stack:
        output = Stack()
        semicolon = Token(
            kind=TokenKind.OPERATOR,
            typeof=TokenType.OP_SEMICOLON,
            value=";"
        )

        divider = self._expr_divider(tokens)

        for expr in divider:
            stack = Stack()
            args_counters = self._count_args(expr)[::-1]

            for i, token in enumerate(expr):
                if token.type == TokenType.NUMBER:
                    output.append(token)
                elif token.type == TokenType.VAR:
                    if i < len(expr)-1 and expr[i+1].type == TokenType.LBRACE:
                        # it's a function!
                        stack.append(self._get_func(token, args_counters.pop()))
                    else:
                        output.append(token)
                elif token.type == TokenType.OP_COMMA:
                    print(token)

                    try:
                        while stack.top.type != TokenType.LBRACE:
                            output.append(stack.pop())
                    except IndexError:
                        raise SyntaxError("missing opening brace or comma") from None
                elif token.kind == TokenKind.OPERATOR:
                    priority = PRIORITIES_TABLE

                    while stack and priority[stack.top.type] >= priority[token.type]:
                        output.append(stack.pop())

                    stack.append(token)
                elif token.type == TokenType.LBRACE:
                    stack.append(token)
                elif token.type == TokenType.RBRACE:
                    try:
                        while stack and stack.top.type != TokenType.LBRACE:
                            output.append(stack.pop())
                    except IndexError:
                        raise SyntaxError("missing opening brace") from None

                    stack.pop()

                    if stack.top.type == TokenType.VAR:
                        # it's a function!
                        output.append(self._get_func(stack.pop(), args_counters.pop()))

            while stack:
                if stack.top.type == TokenType.LBRACE:
                    raise SyntaxError("missing closing brace")

                output.append(stack.pop())

            output.append(semicolon)

        return output[:-1]  # remove trailing semicolon

    def _count_args(self, tokens: Tokens) -> List[int]:
        result = []
        skip_rbraces = 0

        for i, token in enumerate(tokens[1:]):
            if skip_rbraces:
                if token.type == TokenType.RBRACE:
                    skip_rbraces -= 1

                continue

            if token.type == TokenType.LBRACE and tokens[i].type == TokenType.VAR:
                counters = self.__argscounter(tokens[i+2:])
                result.extend(counters)
                skip_rbraces = len(counters)

        return list(map(lambda counter: counter+1, result))

    def __argscounter(self, tokens: Tokens) -> List[int]:
        result = [0]
        skip_rbraces = 0

        for i, token in enumerate(tokens):
            if skip_rbraces:
                if token.type == TokenType.RBRACE:
                    skip_rbraces -= 1

                continue
            elif token.type == TokenType.RBRACE:
                return result

            result[0] += token.type == TokenType.OP_COMMA

            if token.type == TokenType.LBRACE:
                counters = self.__argscounter(tokens[i+1:])
                result.extend(counters)
                skip_rbraces = len(counters)

        return result

    @staticmethod
    def _expr_divider(expr: Tokens) -> Iterator[Tokens]:
        border = 0

        for i, token in enumerate(expr):
            if token.type == TokenType.OP_SEMICOLON:
                yield expr[border:i]
                border = i + 1

        yield expr[border:]

    @staticmethod
    def _get_func(token: Token, argscount: int) -> Token:
        return Token(
            kind=TokenKind.FUNC,
            typeof=TokenType.FUNCCALL,
            value=Func(
                name=token.value,
                argscount=argscount
            )
        )
