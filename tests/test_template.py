"""Test template class."""
import random
import string
import unittest


class TemplateTestCase(unittest.TestCase):
    """Template class Test case."""

    def setUp(self):
        """Create context for tests."""
        first = ''.join(random.choice(string.ascii_letters)
                        for i in range(15))
        second = ''.join(random.choice(string.ascii_letters)
                         for i in range(15))
        self.context = {'first': first, 'second': second}
        self.path = 'tests/fixtures/template.jn2'

    def test_constructor(self):
        """Test tempalate constructor."""
        import hardest.template
        template = hardest.template.Template(self.path,
                                             self.context)
        self.assertIsInstance(template, hardest.template.Template)

    def test_constructor_fails(self):
        """Test constructor fails without args."""
        import hardest.template
        with self.assertRaises(TypeError):
            hardest.template.Template()  # pylint: disable=E1120

    def test_constructor_fails_one_arg(self):
        """Test constructor fails with one args."""
        import hardest.template
        with self.assertRaises(TypeError):
            hardest.template.Template(self.path)  # pylint: disable=E1120

    def test_constructor_fails_bad_path(self):
        """Test constructor with bad file path."""
        import hardest.exceptions
        import hardest.template
        template = hardest.template.Template('FILE_NOT_EXISTS', {})
        with self.assertRaises(hardest.exceptions.TemplateNotFoundException):
            template.render()

    def test_render(self):
        """Test render content."""
        import hardest.template
        template = hardest.template.Template(self.path, self.context)
        should_be = ('start{}end|start{}end'
                     .format(self.context['first'], self.context['second']))
        self.assertEqual(should_be, template.render())
