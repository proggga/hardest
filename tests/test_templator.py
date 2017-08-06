"""Test templator class."""
import random
import string
import unittest

import mock


class TemplatorTestCase(unittest.TestCase):
    """Templator test case."""

    def setUp(self):
        """Set Up."""
        self.package_name = 'hardest'

    def test_constuctor(self):
        """Test templator constructor."""
        import hardest
        instance = hardest.Templator(self.package_name)
        self.assertIsInstance(instance, hardest.Templator)
        self.assertTrue(instance.package_name, self.package_name)

    def test_get_template_path_returns(self):
        """Test get_template_path return path."""
        import hardest
        instance = hardest.Templator(self.package_name)
        template_path = 'templates/tox.ini.jn2'
        full_tox_dir = instance.get_template_path(template_path)
        self.assertTrue(full_tox_dir.endswith(template_path))

    def test_get_template_fails_package(self):
        """Test get_template_path fails."""
        import hardest
        import hardest.exceptions

        package_name = 'strange package name'
        instance = hardest.Templator(package_name)
        template_path = 'templates/tox.ini.jn2'
        with self.assertRaises(hardest.exceptions.TemplateNotFoundException):
            instance.get_template_path(template_path)

    def test_method_fails_template(self):
        """Fails with wrong template."""
        import hardest
        import hardest.exceptions

        instance = hardest.Templator(self.package_name)
        template_path = 'templates/NOTEXIST.jn2'
        with self.assertRaises(hardest.exceptions.TemplateNotFoundException):
            instance.get_template_path(template_path)

    def test_render(self):
        """Test render method."""
        import hardest
        import hardest.exceptions

        instance = hardest.Templator(self.package_name)
        first = ''.join(random.sample(string.ascii_letters, 15))
        second = ''.join(random.sample(string.ascii_letters, 15))
        args = {'first': first, 'second': second}
        mock_path = 'hardest.Templator.get_template_path'

        with mock.patch(mock_path) as patch:
            file_path = 'tests/fixtures/template.jn2'
            patch.return_value = file_path
            content = instance.render(file_path, **args)
            self.assertEqual('start{}end|start{}end'.format(first, second),
                             content)
