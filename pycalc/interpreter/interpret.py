import operator
from functools import reduce
from abc import ABC, abstractmethod
from typing import Optional, Tuple, Union, List

from pycalc.lex import tokenizer as _tokenizer
from pycalc.stack import builder
from pycalc.tokentypes.tokens import Token, Tokens, Function
from pycalc.tokentypes.types import (TokenKind, TokenType, Stack,
                                     Namespace, Number, NamespaceValue,
                                     ArgumentsError, NameNotFoundError)


Value = Union[Number, Function]


class NamespaceStack(Stack):
    def add_namespaces(self, *namespaces: Namespace):
        for namespace in namespaces:
            self.append(namespace)

    def add_namespace(self, namespace: Namespace):
        self.append(namespace)

    def with_add_namespace(self, namespace: Namespace) -> "NamespaceStack":
        self.add_namespace(namespace)
        return self

    def get(self, var: str) -> NamespaceValue:
        for namespace in self[::-1]:
            if var in namespace:
                return namespace[var]

        raise NameNotFoundError(var)

    def set(self, key: str, value: NamespaceValue):
        self.top[key] = value

    def copy(self) -> "NamespaceStack":
        return NamespaceStack(super().copy())

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pop()


class ABCInterpreter(ABC):
    @abstractmethod
    def interpret(self, code: str, namespace: Namespace) -> Value:
        """
        Receives expression as a string and basic namespace.
        This namespace will be in the beginning of the namespaces stack
        Returns the last one element in a stack (if multiple left SyntaxError
        will be raised)
        """


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
                 stackbuilder: Optional[builder.ABCBuilder] = None,
                 ):
        self.tokenizer = tokenize or _tokenizer.Tokenizer()
        self.stackbuilder = stackbuilder or builder.SortingStationBuilder()

    def interpret(self, code: str, namespace: Namespace) -> Value:
        """
        Currently parses only one-line expressions
        """

        tokens = self.tokenizer.tokenize(code)
        stack = self.stackbuilder.build(tokens)
        namespaces = NamespaceStack()
        namespaces.add_namespace(namespace)

        return self._interpreter(stack, namespaces)

    def _interpreter(self, expression: Stack, namespaces: NamespaceStack) -> Value:
        stack = Stack()

        for i, token in enumerate(expression):
            if token.kind == TokenKind.NUMBER or token.type == TokenType.IDENTIFIER:
                stack.append(token)
            elif token.type == TokenType.VAR:
                stack.append(self._token(namespaces.get(token.value)))

            elif token.kind == TokenKind.UNARY_OPERATOR:
                stack.append(self._token(
                    self.unary_executors[token.type](stack.pop().value)
                ))

            elif token.type == TokenType.OP_SEMICOLON:
                if len(stack) > 1:
                    raise SyntaxError("multiple values left in stack")

                stack.pop()
            elif token.type == TokenType.OP_EQ:
                right, left = stack.pop(), stack.pop()
                namespaces.set(left.value, right.value)
                stack.append(right)

            elif token.kind == TokenKind.OPERATOR:
                right, left = stack.pop(), stack.pop()
                stack.append(self._token(
                    self.executors[token.type](left.value, right.value)
                ))
            elif token.type == TokenType.FUNCCALL:
                func = namespaces.get(token.value.name)
                stack, args = self._get_func_args(token.value.argscount, stack)
                call_result = func(*(arg.value for arg in args))
                stack.append(self._token(call_result))
            elif token.type == TokenType.FUNCDEF:
                func_namespace = namespaces.copy()
                func_namespace.add_namespace({})

                func = self._spawn_function(
                    namespace=func_namespace,
                    name=token.value.name,
                    fargs=[tok.value for tok in token.value.args],
                    body=token.value.body
                )

                if token.value.name:
                    # lambdas have no name, so their token.value.name
                    # is just an empty string
                    namespaces.set(token.value.name, func)

                stack.append(Token(
                    kind=TokenKind.FUNC,
                    typeof=TokenType.FUNC,
                    value=func
                ))
            else:
                raise SyntaxError(f"unknown token: {token.type.name}({token.value})")

        result = stack.pop()

        if stack:
            raise SyntaxError("multiple values left in stack")

        return result.value

    def _spawn_function(self,
                        namespace: NamespaceStack,
                        name: str,
                        fargs: List[str],
                        body: Stack) -> Function:
        def real_function(*args) -> Number:
            if not fargs and args:
                raise ArgumentsError("function takes no arguments")
            if len(fargs) != len(args):
                text = (
                    "not enough arguments",
                    "too much arguments"
                )[len(fargs) < len(args)]

                raise ArgumentsError(f"{text}: expected {len(fargs)}, got {len(args)}")

            args_namespace = self._get_args_namespace(fargs, args)

            with namespace.with_add_namespace(args_namespace):
                return self._interpreter(body, namespace)

        return Function(
            name=f"{name}({','.join(fargs)})",
            target=real_function
        )

    @staticmethod
    def _token(num: Number) -> Token:
        if isinstance(num, int):
            return Token(
                kind=TokenKind.NUMBER,
                typeof=TokenType.INTEGER,
                value=int(num)
            )
        elif isinstance(num, float):
            return Token(
                kind=TokenKind.NUMBER,
                typeof=TokenType.FLOAT,
                value=num
            )
        else:
            return Token(
                kind=TokenKind.OTHER,
                typeof=TokenType.OTHER,
                value=num
            )

    @staticmethod
    def _get_func_args(argscount: int, stack: Stack) -> Tuple[Stack, Tokens]:
        if not argscount:
            return stack, []

        return stack[:-argscount], stack[-argscount:]

    @staticmethod
    def _get_args_namespace(fargs, args) -> Namespace:
        return dict(zip(fargs, args))

    @staticmethod
    def _merge_namespaces(*namespaces: Namespace):
        return reduce(lambda a, b: {**a, **b}, namespaces)
