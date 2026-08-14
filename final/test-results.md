# Test Results

**Execution date:** August 13, 2026  
**Runtime:** Python 3.12.13  
**Overall result:** 20 of 20 test methods passed with no failures or errors.

## Expression Parser

Command, run from `Week1-2`:

```powershell
python -m unittest -v
```

Result:

```text
Ran 11 tests in 0.002s
OK
```

The suite passed tests for tokenization, invalid characters, precedence,
parentheses, right-associative exponentiation, unary-minus precedence,
identifiers, decimal numbers, typed AST conversion, incomplete expressions,
missing parentheses, and empty input.

## Functional Portfolio

Command, run from `week2-3`:

```powershell
python -m unittest -v
```

Result:

```text
Ran 9 tests in 0.007s
OK
```

The suite passed tests for recursive algorithms, rejected inputs, sorting and
searching, map/filter/reduce operations, collection transformations,
higher-order functions, text processing, matrices and records, and the AST
constraint that prohibits imperative loops and comprehensions.

## Parser Demonstration

Command, run from the repository root:

```powershell
python Week1-2\math_parser.py "2 + 3 * (x - 4)^2"
```

Result: the command exited successfully and returned JSON containing a
`BinaryOperation` addition root. Its right operand was multiplication by an
exponentiation node representing `(x - 4)^2`, confirming the expected grouping
and operator precedence.
