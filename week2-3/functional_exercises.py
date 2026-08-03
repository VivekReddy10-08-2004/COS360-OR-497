"""Algorithm and data-manipulation exercises in a functional style.

The implementations intentionally contain no ``for``/``while`` statements,
comprehensions, mutation, or variable reassignment.  Inputs are never changed.
"""

from functools import reduce
from operator import add, mul
from typing import Any, Callable, Iterable, Sequence, TypeVar


T = TypeVar("T")
U = TypeVar("U")
K = TypeVar("K")


def factorial(number: int) -> int:
    """Return number!, rejecting negative inputs."""
    if number < 0:
        raise ValueError("factorial is undefined for negative integers")
    return 1 if number < 2 else number * factorial(number - 1)


def fibonacci(number: int) -> int:
    """Return the zero-indexed Fibonacci number using tail recursion."""
    if number < 0:
        raise ValueError("fibonacci is undefined for negative indices")

    def visit(remaining: int, current: int, following: int) -> int:
        return current if remaining == 0 else visit(
            remaining - 1, following, current + following
        )

    return visit(number, 0, 1)


def gcd(left: int, right: int) -> int:
    """Return the non-negative greatest common divisor recursively."""
    return abs(left) if right == 0 else gcd(right, left % right)


def recursive_sum(values: Sequence[int | float]) -> int | float:
    """Sum a sequence recursively."""
    return 0 if not values else values[0] + recursive_sum(values[1:])


def recursive_reverse(values: Sequence[T]) -> list[T]:
    """Return a reversed list without mutating the input."""
    return [] if not values else recursive_reverse(values[1:]) + [values[0]]


def quicksort(values: Sequence[T]) -> list[T]:
    """Return a sorted list using recursive functional quicksort."""
    if len(values) < 2:
        return list(values)
    pivot = values[0]
    tail = values[1:]
    return (
        quicksort(list(filter(lambda item: item < pivot, tail)))
        + list(filter(lambda item: item == pivot, values))
        + quicksort(list(filter(lambda item: item > pivot, tail)))
    )


def merge_sort(values: Sequence[T]) -> list[T]:
    """Return a stable, recursively merge-sorted list."""
    def merge(left: Sequence[T], right: Sequence[T]) -> list[T]:
        if not left or not right:
            return list(left or right)
        return (
            [left[0]] + merge(left[1:], right)
            if left[0] <= right[0]
            else [right[0]] + merge(left, right[1:])
        )

    middle = len(values) // 2
    return list(values) if len(values) < 2 else merge(
        merge_sort(values[:middle]), merge_sort(values[middle:])
    )


def binary_search(values: Sequence[T], target: T) -> int:
    """Return target's index in a sorted sequence, or -1 when absent."""
    def search(low: int, high: int) -> int:
        if low > high:
            return -1
        middle = (low + high) // 2
        return (
            middle
            if values[middle] == target
            else search(middle + 1, high)
            if values[middle] < target
            else search(low, middle - 1)
        )

    return search(0, len(values) - 1)


def squares(values: Iterable[int | float]) -> list[int | float]:
    return list(map(lambda value: value * value, values))


def even_numbers(values: Iterable[int]) -> list[int]:
    return list(filter(lambda value: value % 2 == 0, values))


def product(values: Iterable[int | float]) -> int | float:
    return reduce(mul, values, 1)


def flatten(groups: Iterable[Iterable[T]]) -> list[T]:
    return reduce(add, map(list, groups), [])


def unique(values: Sequence[T]) -> list[T]:
    """Remove duplicates while preserving first-seen order."""
    return [] if not values else [values[0]] + unique(
        list(filter(lambda item: item != values[0], values[1:]))
    )


def frequency(values: Iterable[T]) -> dict[T, int]:
    """Count values without mutating an accumulator."""
    return reduce(
        lambda counts, item: counts | {item: counts.get(item, 0) + 1}, values, {}
    )


def group_by(values: Iterable[T], key: Callable[[T], K]) -> dict[K, list[T]]:
    """Group values by a derived key without mutating an accumulator."""
    return reduce(
        lambda groups, item: groups
        | {key(item): groups.get(key(item), []) + [item]},
        values,
        {},
    )


def compose(*functions: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """Compose functions right-to-left; compose() is the identity."""
    return lambda value: reduce(lambda result, function: function(result),
                                reversed(functions), value)


def pipe(value: T, *functions: Callable[[Any], Any]) -> Any:
    """Pass a value through functions from left to right."""
    return reduce(lambda result, function: function(result), functions, value)


def normalize_words(text: str) -> list[str]:
    """Extract lowercase alphanumeric words from text."""
    return "".join(map(lambda char: char.lower() if char.isalnum() else " ", text)).split()


def word_frequencies(text: str) -> dict[str, int]:
    return frequency(normalize_words(text))


def is_palindrome(text: str) -> bool:
    normalized = "".join(filter(str.isalnum, map(str.lower, text)))
    return normalized == normalized[::-1]


def transpose(matrix: Sequence[Sequence[T]]) -> list[list[T]]:
    """Transpose a rectangular matrix; an empty matrix stays empty."""
    if not matrix:
        return []
    if not all(map(lambda row: len(row) == len(matrix[0]), matrix)):
        raise ValueError("matrix must be rectangular")
    return list(map(list, zip(*matrix)))


def select_fields(records: Iterable[dict[str, T]], *fields: str) -> list[dict[str, T]]:
    """Project records onto the requested fields, ignoring missing fields."""
    return list(map(
        lambda record: dict(filter(lambda pair: pair[0] in fields, record.items())),
        records,
    ))


def average_by(records: Iterable[dict[str, Any]], group: str,
               value: str) -> dict[Any, float]:
    """Compute a numeric field's average for each group."""
    totals = reduce(
        lambda result, record: result
        | {record[group]: (
            result.get(record[group], (0, 0))[0] + record[value],
            result.get(record[group], (0, 0))[1] + 1,
        )},
        records,
        {},
    )
    return dict(map(lambda pair: (pair[0], pair[1][0] / pair[1][1]), totals.items()))
