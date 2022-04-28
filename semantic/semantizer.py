from abc import ABC, abstractmethod
from typing import Optional, List

from tokentypes.tokens import Token, Tokens, Lexeme, Lexemes, FuncCall
from tokentypes.types import (LexemeType, TokenType, UNARY_OPERATORS,
                              OPERATORS_TABLE, OPERATOR)


class ABCSemantizer(ABC):
    @abstractmethod
    def semantize(self, lexemes: Lexemes) -> Tokens:
        ...


class Semantizer:
    def __init__(self):
        self.tokens: Tokens = []

    def semantize(self, lexemes: Lexemes) -> Tokens:
        if not lexemes:
            return []

        tokens = self._perform_braces(lexemes)
        unary = self._perform_unary(tokens)
        funcs = self._perform_functions(unary)

        return funcs

    def _perform_braces(self, lexemes: Lexemes) -> Tokens:
        """
        A first stage of semantic. It just converts lexemes to just tokens,
        at the same time merging in-braces expressions
        """

        bracesbuf: Lexemes = []
        result: Tokens = []
        nested_braces = 0

        for lexeme in lexemes:
            if lexeme.type == LexemeType.RBRACE:
                if nested_braces:
                    nested_braces -= 1
                    bracesbuf.append(lexeme)
                    continue

                if not bracesbuf:
                    raise SyntaxError("found closing brace without opening")

                result.append(Token(
                    typeof=TokenType.BRACE_EXPR,
                    unary=None,  # will be set later, on a second stage
                    value=self.semantize(bracesbuf[1:])
                ))
                bracesbuf.clear()
            elif lexeme.type == LexemeType.LBRACE and bracesbuf:
                nested_braces += 1
                bracesbuf.append(lexeme)
            elif lexeme.type == LexemeType.LBRACE or bracesbuf:
                bracesbuf.append(lexeme)
            else:
                result.append(Token(
                    typeof=self._get_lexeme_type(lexeme),
                    unary=None,
                    value=float(lexeme.value) if lexeme.type == LexemeType.NUMBER else lexeme.value
                ))

        if bracesbuf:
            print("Braces buffer:", bracesbuf)
            raise SyntaxError("no closing brace found")

        return result

    @staticmethod
    def _get_lexeme_type(lexeme: Lexeme) -> TokenType:
        if lexeme.type == LexemeType.NUMBER:
            return TokenType.NUMBER
        elif lexeme.type == LexemeType.LITERAL:
            return TokenType.LITERAL
        elif lexeme.type == LexemeType.COMMA:
            return TokenType.COMMA
        elif lexeme.type == LexemeType.OPERATOR:
            return OPERATORS_TABLE[lexeme.value]

        raise ValueError("unrecognized operator: " + lexeme.value)

    def _perform_unary(self, tokens: Tokens) -> Tokens:
        """
        A second stage of semantic. It just determines a final unary of a token
        """

        result: Tokens = []
        unarybuf: Tokens = []
        startswith_unary = tokens[0].type & OPERATOR

        for token in tokens:
            if token.type & OPERATOR:
                unarybuf.append(token)
            elif unarybuf:
                if startswith_unary:
                    token.unary = self._calculate_final_unary(unarybuf)
                    startswith_unary = False
                else:
                    result.append(unarybuf[0])
                    token.unary = self._calculate_final_unary(unarybuf[1:])

                result.append(token)
                unarybuf.clear()
            else:
                result.append(token)

        if unarybuf:
            raise SyntaxError("missing last operand")

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
        return TokenType.OP_SUB if subs & 1 else TokenType.OP_ADD

    def _perform_functions(self, tokens: Tokens) -> Tokens:
        """
        Finally, third, and the last one stage of semantic
        Performing LITERAL+BRACE_EXPR to function calls
        """

        result: Tokens = []
        skip = False

        for index, token in enumerate(tokens[:-1]):
            if skip:
                skip = False
                continue

            if token.type == TokenType.LITERAL and tokens[index+1].type == TokenType.BRACE_EXPR:
                # LITERAL, BRACE_EXPR = FUNC
                result.append(Token(
                    typeof=TokenType.FUNC,
                    value=FuncCall(
                        name=token.value,
                        args=self._get_func_args(tokens[index+1].value)
                    ),
                    unary=token.unary
                ))

                skip = True
            else:
                result.append(token)

        if not skip:
            result.append(tokens[-1])

        return result

    @staticmethod
    def _get_func_args(args_tokens: Tokens) -> List[Tokens]:
        """
        Returns a list of expressions that are separated by a comma
        """

        args: List[Tokens] = []
        prev_index = 0
        nested_braces = 0

        for index, token in enumerate(args_tokens):
            if token.type == TokenType.COMMA and not nested_braces:
                args.append(args_tokens[prev_index:index])
                prev_index = index + 1

        args.append(args_tokens[prev_index:])

        return args
