import operator
from functools import reduce
from abc import ABC, abstractmethod
from typing import Optional, Callable, Tuple

from pycalc.lex import tokenizer as _tokenizer
from pycalc.stack import builder
from pycalc.tokentypes.tokens import Token, Tokens
from pycalc.tokentypes.types import (TokenKind, TokenType, Stack,
                                     Namespace, Number, ArgumentsError)


class ABCInterpreter(ABC):
    @abstractmethod
    def interpret(self, code: str, namespace: Namespace) -> Number:
        ...


class Interpreter(ABCInterpreter):
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

    def __init__(self,
                 tokenize: Optional[_tokenizer.ABCTokenizer] = None,
                 stackbuilder: Optional[builder.ABCBuilder] = None):
        self.tokenizer = tokenize or _tokenizer.Tokenizer()
        self.stackbuilder = stackbuilder or builder.SortingStationBuilder()

    def interpret(self, code: str, namespace: Namespace) -> Number:
        """
        Currently parses only one-line expressions
        """

        tokens = self.tokenizer.tokenize(code)
        stack = self.stackbuilder.build(tokens)

        return self._interpreter(stack, namespace)

    def _interpreter(self, expression: Stack, namespace: Namespace) -> Number:
        stack = Stack()

        for i, token in enumerate(expression):
            if token.type in (TokenType.NUMBER, TokenType.IDENTIFIER):
                stack.append(token)
            elif token.type == TokenType.VAR:
                stack.append(self._number(namespace[token.value]))

            elif token.kind == TokenKind.UNARY_OPERATOR:
                stack.append(self._number(
                    self.unary_executors[token.type](stack.pop().value)
                ))

            elif token.type == TokenType.OP_SEMICOLON:
                if len(stack) > 1:
                    raise SyntaxError("multiple values left in stack")

                stack.pop()
            elif token.type == TokenType.OP_EQ:
                right, left = stack.pop(), stack.pop()
                namespace[left.value] = right.value
                stack.append(right)

            elif token.kind == TokenKind.OPERATOR:
                right, left = stack.pop(), stack.pop()
                stack.append(self._number(
                    float(self.executors[token.type](left.value, right.value))
                ))
            elif token.type == TokenType.FUNCCALL:
                func = namespace[token.value.name]
                stack, args = self._get_func_args(token.value.argscount, stack)
                call_result = func(*(token.value for token in args))
                stack.append(self._number(call_result))
            elif token.type == TokenType.FUNCDEF:
                namespace[token.value.name] = self._spawn_function(
                    namespace=namespace,
                    fargs=[tok.value for tok in token.value.args],
                    body=expression[i+1:]
                )

                return 0
            else:
                raise SyntaxError(f"unknown token: {token.type.name}({token.value})")

        result = stack.pop()

        if stack:
            raise SyntaxError("multiple values left in stack")

        return result.value

    def _spawn_function(self, namespace: Namespace, fargs: Tokens, body: Stack) -> Callable:
        def real_function(*args) -> Number:
            if len(fargs) != len(args):
                text = (
                    "not enough arguments",
                    "too much arguments"
                )[len(fargs) < len(args)]

                raise ArgumentsError(
                    f"{text}: expected {len(fargs)}, got {len(args)}",
                    (0, 0)  # TODO: how to add position here?
                )

            return self._interpreter(body, self._merge_namespaces(
                namespace, self._get_args_namespace(fargs, args)
            ))

        return real_function

    @staticmethod
    def _number(num: Number) -> Token:
        return Token(
            kind=TokenKind.NUMBER,
            typeof=TokenType.NUMBER,
            value=num
        )

    @staticmethod
    def _get_func_args(argscount: int, stack: Stack) -> Tuple[Stack, Tokens]:
        return stack[:-argscount], stack[-argscount:]

    @staticmethod
    def _get_args_namespace(fargs, args) -> Namespace:
        return dict(zip(fargs, args))

    @staticmethod
    def _merge_namespaces(*namespaces: Namespace):
        return reduce(lambda a, b: {**a, **b}, namespaces)
