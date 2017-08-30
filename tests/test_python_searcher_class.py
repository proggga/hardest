"""Tests class (constructor and other data)."""
import os
import unittest


class PythonSearcherClassTestCase(unittest.TestCase):
    """Test case for it."""

    def test_construtor_without_args(self):
        # type: () -> None
        """Test constuctor without params."""
        import hardest.python_searcher as pysearch
        instance = pysearch.PythonSearcher()
        some_env = os.environ.copy()
        self.assertEqual(instance.env, some_env)

    def test_constr_bad_validator(self):
        # type: () -> None
        """Test constuctor with bad validator."""
        import hardest.python_searcher as pysearch
        with self.assertRaises(TypeError):  # type: ignore
            pysearch.PythonSearcher(validator='not validator')  # type: ignore
