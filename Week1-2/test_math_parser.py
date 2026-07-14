import unittest

from math_parser import (
    BinaryOperation,
    Identifier,
    Lexer,
    LexerError,
    Number,
    ParserError,
    TokenType,
    UnaryOperation,
    ast_to_dict,
    parse_expression,
)


class LexerTests(unittest.TestCase):
    def test_tokenizes_numbers_names_and_operators(self) -> None:
        tokens = Lexer("total_2 + 3.5 * (x - .25)").tokenize()
        self.assertEqual(
            [token.type for token in tokens],
            [
                TokenType.IDENTIFIER,
                TokenType.PLUS,
                TokenType.NUMBER,
                TokenType.STAR,
                TokenType.LEFT_PAREN,
                TokenType.IDENTIFIER,
                TokenType.MINUS,
                TokenType.NUMBER,
                TokenType.RIGHT_PAREN,
                TokenType.EOF,
            ],
        )

    def test_rejects_invalid_character(self) -> None:
        with self.assertRaisesRegex(LexerError, "position 2"):
            Lexer("2 @ 3").tokenize()


class ParserTests(unittest.TestCase):
    def test_honors_operator_precedence(self) -> None:
        self.assertEqual(
            parse_expression("2 + 3 * 4"),
            BinaryOperation(
                "+", Number(2), BinaryOperation("*", Number(3), Number(4))
            ),
        )

    def test_parentheses_override_precedence(self) -> None:
        self.assertEqual(
            parse_expression("(2 + 3) * 4"),
            BinaryOperation(
                "*", BinaryOperation("+", Number(2), Number(3)), Number(4)
            ),
        )

    def test_exponentiation_is_right_associative(self) -> None:
        self.assertEqual(
            parse_expression("2 ^ 3 ^ 2"),
            BinaryOperation(
                "^", Number(2), BinaryOperation("^", Number(3), Number(2))
            ),
        )

    def test_exponentiation_binds_more_tightly_than_unary_minus(self) -> None:
        self.assertEqual(
            parse_expression("-2^2"),
            UnaryOperation("-", BinaryOperation("^", Number(2), Number(2))),
        )

    def test_parses_identifiers_and_decimal_numbers(self) -> None:
        self.assertEqual(
            parse_expression("rate / 2.5"),
            BinaryOperation("/", Identifier("rate"), Number(2.5)),
        )

    def test_converts_ast_to_typed_dictionary(self) -> None:
        self.assertEqual(
            ast_to_dict(parse_expression("-x")),
            {
                "operator": "-",
                "operand": {"name": "x", "type": "Identifier"},
                "type": "UnaryOperation",
            },
        )

    def test_rejects_incomplete_expression(self) -> None:
        with self.assertRaisesRegex(ParserError, "end of input"):
            parse_expression("2 +")

    def test_rejects_missing_closing_parenthesis(self) -> None:
        with self.assertRaisesRegex(ParserError, "Expected '\\)'"):
            parse_expression("(2 + 3")

    def test_rejects_empty_input(self) -> None:
        with self.assertRaisesRegex(ParserError, "end of input"):
            parse_expression("")


if __name__ == "__main__":
    unittest.main()
