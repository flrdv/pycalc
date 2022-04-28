from typing import List, Iterable
from abc import ABC, abstractmethod

from tokentypes.tokens import Token, Tokens, Context
from tokentypes.types import OPERATOR, PRIORITIES_TABLE, TokenType


class Node(ABC):
    @abstractmethod
    def execute(self, ast_builder: "ABCAbstractSyntaxTree", context: Context) -> Token:
        ...


class BinOp(Node):
    _ops_performers = {
        TokenType.OP_ADD: lambda left, right: left + right,
        TokenType.OP_SUB: lambda left, right: left - right,
        TokenType.OP_DIV: lambda left, right: left / right,
        TokenType.OP_MUL: lambda left, right: left * right,
    }

    def __init__(self, left: Node, op: Token, right: Node):
        self.left = left
        self.op = op
        self.right = right

    def execute(self, ast_builder: "ABCAbstractSyntaxTree", context: Context) -> Token:
        """
        Must return a token with type NUMBER
        """

        left = self.left

        if isinstance(left, Node):
            left = left.execute(ast_builder, context)

        right = self.right

        if isinstance(right, Node):
            right = right.execute(ast_builder, context)

        return performed_number(self._perform_op(
            _perform_token(ast_builder, left, context),
            _perform_token(ast_builder, right, context)
        ))

    def _perform_op(self, left: Token, right: Token) -> float:
        if self.op.type == TokenType.OP_POW:
            print("Hello here!")
            # right and left tokens are already performed
            right_value = _get_unarized_value(right.value, right.unary)

            return _get_unarized_value(left.value ** right_value, left.unary)

        return self._ops_performers[self.op.type](
            _get_unarized_value(left.value, left.unary),
            _get_unarized_value(right.value, right.unary)
        )


class MonoOp(Node):
    def __init__(self, token: Token):
        self.token = token

    def execute(self, ast_builder: "ABCAbstractSyntaxTree", context: Context) -> Token:
        performed_token = _perform_token(ast_builder, self.token, context)

        return performed_number(_get_unarized_value(
               performed_token.value, performed_token.unary
            ))


class ABCAbstractSyntaxTree(ABC):
    @abstractmethod
    def build(self, tokens: Tokens) -> Node:
        ...


class AST(ABCAbstractSyntaxTree):
    def build(self, tokens: Tokens) -> Node:
        if not tokens:
            raise ValueError("unable to build ast of an empty list of tokens")

        if len(tokens) == 1:
            token = tokens[0]

            if token.type == TokenType.BRACE_EXPR:
                return self.build(token.value)

            return MonoOp(tokens[0])

        try:
            op_index = self._pick_youngest_op(tokens)
        except IndexError:
            raise SyntaxError("expression must contain operators") from None

        if op_index == 0 or op_index + 1 == len(tokens):
            raise SyntaxError("expression cannot start or end with operator")

        return BinOp(
            left=self.build(tokens[:op_index]),
            op=tokens[op_index],
            right=self.build(tokens[op_index+1:])
        )

    @staticmethod
    def _pick_youngest_op(tokens: Tokens) -> int:
        """
        Returns an index of the operator with the least priority

        Implemented as a single expression :)
        """

        return tokens.index(sorted(
            filter(lambda token: OPERATOR & token.type, tokens),
            key=lambda token: PRIORITIES_TABLE[token.type],
            reverse=True
        )[-1])


def _perform_token(ast: ABCAbstractSyntaxTree, token: Token, context: Context) -> Token:
    """
    Takes any token as an input, and makes token with a type of number
    This means that we're performing such actions as literals and
    function calls
    """

    if token.type == TokenType.NUMBER:
        return token

    if token.type == TokenType.LITERAL:
        value = context[token.value]
    elif token.type == TokenType.FUNC:
        func = context[token.value.name]

        if not callable(func):
            raise TypeError(f'"{token.value.name}" is not a callable object')

        value = func(*_perform_function_args(ast, token.value.args, context))
    else:
        value = token.value

    return Token(
        typeof=TokenType.NUMBER,
        unary=token.unary,
        value=value
    )


def _perform_function_args(ast_builder: ABCAbstractSyntaxTree,
                           args: List[Tokens], context: Context) -> Iterable[float]:
    # hehe again you got scammed
    # actually, this code just builds an ast for each argument, and
    # instantly executes it as the only thing we need is the operation's result
    return map(lambda arg: ast_builder.build(arg).execute(ast_builder, context).value, args)


def _get_unarized_value(value: float, unary: TokenType) -> float:
    """
    Returns a value of the token, applying unary operation.
    Passed token's type must be a number
    """

    if unary is None:
        return value
    elif unary == TokenType.OP_ADD:
        return +value
    elif unary == TokenType.OP_SUB:
        return -value

    raise TypeError("unary must be None, OP_ADD or OP_SUB")


def performed_number(value: float) -> Token:
    """
    Just a sugar
    """

    return Token(
        typeof=TokenType.NUMBER,
        unary=None,
        value=value
    )
