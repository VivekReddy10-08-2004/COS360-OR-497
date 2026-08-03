# Purely Functional Python Exercises

This directory contains a broad set of algorithm and data-manipulation
exercises implemented without `for`/`while` statements, comprehensions,
mutation, or variable reassignment. The solutions use recursion and the
higher-order functions `map`, `filter`, and `functools.reduce`.

The exercises cover recursion, sorting, searching, collection transforms,
function composition, text processing, matrices, and record aggregation.
Every function returns a new value and leaves its inputs unchanged.

Run the suite from this directory with Python 3.10 or newer:

```powershell
python -m unittest -v
```

The final test parses the implementation's syntax tree to enforce the ban on
imperative loops and comprehensions.
