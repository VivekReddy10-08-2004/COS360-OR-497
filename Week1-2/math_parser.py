"""A small, dependency-free lexer and recursive-descent math parser.

Grammar (``^`` is right-associative)::

    expression  -> term (("+" | "-") term)*
    term        -> unary (("*" | "/") unary)*
    unary       -> ("+" | "-") unary | power
    power       -> primary ("^" unary)?
    primary     -> NUMBER | IDENTIFIER | "(" expression ")"
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from enum import Enum, auto
from typing import TypeAlias


class TokenType(Enum):
    NUMBER = auto()
    IDENTIFIER = auto()
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    CARET = auto()
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    EOF = auto()


@dataclass(frozen=True)
class Token:
    type: TokenType
    lexeme: str
    position: int


class LexerError(ValueError):
    """Raised when an expression contains an invalid character or number."""


class ParserError(ValueError):
    """Raised when a token sequence does not match the grammar."""


class Lexer:
    """Convert mathematical source text into a stream of tokens."""

    _SINGLE_CHARACTER_TOKENS = {
        "+": TokenType.PLUS,
        "-": TokenType.MINUS,
        "*": TokenType.STAR,
        "/": TokenType.SLASH,
        "^": TokenType.CARET,
        "(": TokenType.LEFT_PAREN,
        ")": TokenType.RIGHT_PAREN,
    }

    def __init__(self, source: str) -> None:
        self.source = source
        self.current = 0

    def tokenize(self) -> list[Token]:
        tokens: list[Token] = []
        while self.current < len(self.source):
            character = self.source[self.current]

            if character.isspace():
                self.current += 1
            elif character in self._SINGLE_CHARACTER_TOKENS:
                tokens.append(
                    Token(
                        self._SINGLE_CHARACTER_TOKENS[character],
                        character,
                        self.current,
                    )
                )
                self.current += 1
            elif character.isdigit() or character == ".":
                tokens.append(self._number())
            elif character.isalpha() or character == "_":
                tokens.append(self._identifier())
            else:
                raise LexerError(
                    f"Unexpected character {character!r} at position {self.current}"
                )

        tokens.append(Token(TokenType.EOF, "", len(self.source)))
        return tokens

    def _number(self) -> Token:
        start = self.current
        dot_seen = False

        while self.current < len(self.source):
            character = self.source[self.current]
            if character == ".":
                if dot_seen:
                    break
                dot_seen = True
            elif not character.isdigit():
                break
            self.current += 1

        lexeme = self.source[start : self.current]
        if lexeme == ".":
            raise LexerError(f"Invalid number '.' at position {start}")
        return Token(TokenType.NUMBER, lexeme, start)

    def _identifier(self) -> Token:
        start = self.current
        while self.current < len(self.source):
            character = self.source[self.current]
            if not (character.isalnum() or character == "_"):
                break
            self.current += 1
        return Token(TokenType.IDENTIFIER, self.source[start : self.current], start)


@dataclass(frozen=True)
class Number:
    value: int | float


@dataclass(frozen=True)
class Identifier:
    name: str


@dataclass(frozen=True)
class UnaryOperation:
    operator: str
    operand: "Expression"


@dataclass(frozen=True)
class BinaryOperation:
    operator: str
    left: "Expression"
    right: "Expression"


Expression: TypeAlias = Number | Identifier | UnaryOperation | BinaryOperation


class Parser:
    """Build an AST from tokens using recursive descent."""

    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.current = 0

    def parse(self) -> Expression:
        expression = self._expression()
        if not self._check(TokenType.EOF):
            token = self._peek()
            raise ParserError(
                f"Unexpected token {token.lexeme!r} at position {token.position}"
            )
        return expression

    def _expression(self) -> Expression:
        expression = self._term()
        while self._match(TokenType.PLUS, TokenType.MINUS):
            operator = self._previous().lexeme
            expression = BinaryOperation(operator, expression, self._term())
        return expression

    def _term(self) -> Expression:
        expression = self._unary()
        while self._match(TokenType.STAR, TokenType.SLASH):
            operator = self._previous().lexeme
            expression = BinaryOperation(operator, expression, self._unary())
        return expression

    def _unary(self) -> Expression:
        if self._match(TokenType.PLUS, TokenType.MINUS):
            return UnaryOperation(self._previous().lexeme, self._unary())
        return self._power()

    def _power(self) -> Expression:
        expression = self._primary()
        if self._match(TokenType.CARET):
            expression = BinaryOperation("^", expression, self._unary())
        return expression

    def _primary(self) -> Expression:
        if self._match(TokenType.NUMBER):
            text = self._previous().lexeme
            return Number(float(text) if "." in text else int(text))

        if self._match(TokenType.IDENTIFIER):
            return Identifier(self._previous().lexeme)

        if self._match(TokenType.LEFT_PAREN):
            expression = self._expression()
            if not self._match(TokenType.RIGHT_PAREN):
                token = self._peek()
                raise ParserError(f"Expected ')' at position {token.position}")
            return expression

        token = self._peek()
        found = "end of input" if token.type is TokenType.EOF else repr(token.lexeme)
        raise ParserError(
            f"Expected a number, identifier, or '(' at position "
            f"{token.position}; found {found}"
        )

    def _match(self, *types: TokenType) -> bool:
        if any(self._check(token_type) for token_type in types):
            self.current += 1
            return True
        return False

    def _check(self, token_type: TokenType) -> bool:
        return self._peek().type is token_type

    def _peek(self) -> Token:
        return self.tokens[self.current]

    def _previous(self) -> Token:
        return self.tokens[self.current - 1]


def parse_expression(source: str) -> Expression:
    """Lex and parse *source*, returning the root AST node."""

    return Parser(Lexer(source).tokenize()).parse()


def ast_to_dict(expression: Expression) -> dict[str, object]:
    """Return a JSON-serializable representation with explicit node types."""

    result = asdict(expression)
    result["type"] = type(expression).__name__

    if isinstance(expression, UnaryOperation):
        result["operand"] = ast_to_dict(expression.operand)
    elif isinstance(expression, BinaryOperation):
        result["left"] = ast_to_dict(expression.left)
        result["right"] = ast_to_dict(expression.right)
    return result


def main() -> int:
    argument_parser = argparse.ArgumentParser(
        description="Parse a mathematical expression and print its AST as JSON."
    )
    argument_parser.add_argument("expression", help='expression such as "2 + 3 * x"')
    args = argument_parser.parse_args()

    try:
        tree = parse_expression(args.expression)
    except (LexerError, ParserError) as error:
        argument_parser.error(str(error))

    print(json.dumps(ast_to_dict(tree), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
