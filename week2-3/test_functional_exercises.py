import ast
import unittest
from pathlib import Path

import functional_exercises as f


class FunctionalExercisesTests(unittest.TestCase):
    def test_recursive_algorithms(self):
        self.assertEqual(f.factorial(6), 720)
        self.assertEqual(f.fibonacci(10), 55)
        self.assertEqual(f.gcd(-54, 24), 6)
        self.assertEqual(f.recursive_sum([1, 2, 3, 4]), 10)
        self.assertEqual(f.recursive_reverse((1, 2, 3)), [3, 2, 1])

    def test_invalid_recursive_inputs(self):
        self.assertRaises(ValueError, f.factorial, -1)
        self.assertRaises(ValueError, f.fibonacci, -1)

    def test_sort_and_search(self):
        values = [5, 1, 3, 3, -2, 8]
        expected = [-2, 1, 3, 3, 5, 8]
        self.assertEqual(f.quicksort(values), expected)
        self.assertEqual(f.merge_sort(values), expected)
        self.assertEqual(values, [5, 1, 3, 3, -2, 8])
        self.assertIn(f.binary_search(expected, 3), (2, 3))
        self.assertEqual(f.binary_search(expected, 7), -1)

    def test_map_filter_reduce_exercises(self):
        self.assertEqual(f.squares([1, -2, 3]), [1, 4, 9])
        self.assertEqual(f.even_numbers(range(7)), [0, 2, 4, 6])
        self.assertEqual(f.product([2, 3, 4]), 24)
        self.assertEqual(f.product([]), 1)
        self.assertEqual(f.flatten([[1, 2], (), [3]]), [1, 2, 3])

    def test_collection_transformations(self):
        self.assertEqual(f.unique([2, 1, 2, 3, 1]), [2, 1, 3])
        self.assertEqual(f.frequency("banana"), {"b": 1, "a": 3, "n": 2})
        self.assertEqual(
            f.group_by(["ant", "ape", "bear"], lambda word: word[0]),
            {"a": ["ant", "ape"], "b": ["bear"]},
        )

    def test_higher_order_functions(self):
        double = lambda value: value * 2
        increment = lambda value: value + 1
        self.assertEqual(f.compose(double, increment)(3), 8)
        self.assertEqual(f.pipe(3, double, increment), 7)
        self.assertEqual(f.compose()(3), 3)

    def test_text_processing(self):
        self.assertEqual(f.normalize_words("Hello, HELLO! 42"), ["hello", "hello", "42"])
        self.assertEqual(f.word_frequencies("To be, or not to be."),
                         {"to": 2, "be": 2, "or": 1, "not": 1})
        self.assertTrue(f.is_palindrome("A man, a plan, a canal: Panama!"))
        self.assertFalse(f.is_palindrome("functional"))

    def test_matrix_and_records(self):
        self.assertEqual(f.transpose([[1, 2, 3], [4, 5, 6]]),
                         [[1, 4], [2, 5], [3, 6]])
        self.assertRaises(ValueError, f.transpose, [[1], [2, 3]])
        records = [
            {"name": "Ada", "team": "A", "score": 90},
            {"name": "Linus", "team": "B", "score": 70},
            {"name": "Grace", "team": "A", "score": 80},
        ]
        self.assertEqual(f.select_fields(records, "name", "score")[0],
                         {"name": "Ada", "score": 90})
        self.assertEqual(f.average_by(records, "team", "score"),
                         {"A": 85.0, "B": 70.0})

    def test_implementation_has_no_imperative_loops_or_comprehensions(self):
        tree = ast.parse(Path(f.__file__).read_text(encoding="utf-8"))
        forbidden = (ast.For, ast.AsyncFor, ast.While, ast.ListComp,
                     ast.SetComp, ast.DictComp, ast.GeneratorExp)
        self.assertFalse(list(filter(lambda node: isinstance(node, forbidden), ast.walk(tree))))


if __name__ == "__main__":
    unittest.main()
