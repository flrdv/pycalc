import operator
from abc import ABC, abstractmethod
from typing import Optional, Dict, Union

from pycalc.lex import tokenizer as _tokenizer
from pycalc.stack import builder
from pycalc.tokentypes.tokens import Token
from pycalc.tokentypes.types import TokenKind, TokenType


NamespaceValue = Union[int, float, callable]
Namespace = Dict[str, NamespaceValue]


class ABCInterpreter(ABC):
    @abstractmethod
    def interpret(self, code: str) -> int:
        ...


class Interpreter(ABCInterpreter):
    def __init__(self,
                 variables: Namespace = None,
                 tokenize: Optional[_tokenizer.ABCTokenizer] = None,
                 stackbuilder: Optional[builder.ABCBuilder] = None):
        self.variables = variables or {}
        self.tokenizer = tokenize or _tokenizer.Tokenizer()
        self.stackbuilder = stackbuilder or builder.SortingStationBuilder()

    def interpret(self, code: str) -> int:
        """
        Currently parses only one-line expressions
        """

        tokens = self.tokenizer.tokenize(code)
        stack = self.stackbuilder.build(tokens)

        return self._interpreter(stack, self.variables)

    def _interpreter(self, expression: builder.Stack, namespace: Namespace) -> int:
        unary_executors = {
            TokenType.UN_POS: operator.pos,
            TokenType.UN_NEG: operator.neg,
        }
        executors = {
            TokenType.OP_ADD: operator.add,
            TokenType.OP_SUB: operator.sub,

            TokenType.OP_DIV:         operator.truediv,
            TokenType.OP_FLOORDIV:    operator.floordiv,  # it's me!
            TokenType.OP_MUL:         operator.mul,
            TokenType.OP_MOD:         operator.mod,
            TokenType.OP_LSHIFT:      operator.lshift,
            TokenType.OP_RSHIFT:      operator.rshift,
            TokenType.OP_BITWISE_AND: operator.and_,
            TokenType.OP_BITWISE_OR:  operator.or_,
            TokenType.OP_BITWISE_XOR: operator.xor,

            TokenType.OP_EQEQ:  operator.eq,
            TokenType.OP_NOTEQ: operator.ne,

            TokenType.OP_POW: operator.pow,
        }

        stack = []

        for token in expression:
            if token.type in (TokenType.NUMBER, TokenType.VARDECL):
                stack.append(token)
            elif token.type == TokenType.VAR:
                stack.append(namespace[token.value])

            elif token.kind == TokenKind.UNARY_OPERATOR:
                tok = stack.pop()
                stack.append(unary_executors[tok.type](tok.value))

            elif token.type == TokenType.OP_SEMICOLON:
                if len(stack) > 1:
                    raise SyntaxError("multiple values left in stack")

                stack.pop()
            elif token.type == TokenType.OP_EQ:
                right, left = stack.pop(), stack.pop()
                namespace[left.value] = right
                stack.append(right)

            elif token.kind == TokenKind.OPERATOR:
                right, left = stack.pop(), stack.pop()
                stack.append(self._number(
                    float(executors[token.type](left.value, right.value))
                ))
            elif token.type == TokenType.FUNCCALL:
                func = namespace[token.value.name]
                stack, args = stack[:-token.value.argscount], stack[-token.value.argscount:]
                call_result = func(*(token.value for token in args))
                stack.append(self._number(call_result))
            else:
                raise SyntaxError(f"unknown token: {token.type.name}({token.value})")

        result = stack.pop()

        if stack:
            raise SyntaxError("multiple values left in stack")

        return result.value

    @staticmethod
    def _number(num: Union[int, float]) -> Token:
        return Token(
            kind=TokenKind.NUMBER,
            typeof=TokenType.NUMBER,
            value=num
        )
