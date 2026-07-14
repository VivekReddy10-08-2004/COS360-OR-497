# Mathematical Expression Parser

This project implements the activity in `To-Do.md`: a lexer and recursive
descent parser written from scratch in Python. It accepts integers, decimal
numbers, identifiers, parentheses, unary signs, and the operators `+`, `-`,
`*`, `/`, and `^`.

Developed in Python 3.14
Run it with Python 3.10 or newer:

```powershell
python math_parser.py "2 + 3 * (x - 4)^2"
```

The command prints the Abstract Syntax Tree (AST) as formatted JSON. For
example, `2 + 3 * x` has a `BinaryOperation` (`+`) at its root, whose right
child is another `BinaryOperation` (`*`), reflecting multiplication's higher
precedence.

Run the test suite with:

```powershell
python -m unittest -v
```

## Grammar

```text
expression  -> term (("+" | "-") term)*
term        -> unary (("*" | "/") unary)*
unary       -> ("+" | "-") unary | power
power       -> primary ("^" unary)?
primary     -> NUMBER | IDENTIFIER | "(" expression ")"
```

Exponentiation is right-associative, so `2 ^ 3 ^ 2` parses as
`2 ^ (3 ^ 2)`. It also has higher precedence than unary minus, so `-2^2`
parses as `-(2^2)`.
