"""Test templator class."""
import random
import string
import unittest

import mock

from hardest.exceptions import TemplateNotFoundException
from hardest.templator import Templator


class TemplatorTestCase(unittest.TestCase):
    """Templator test case."""

    def test_constuctor(self):
        """Test templator constructor."""
        package_name = 'hardest'
        instance = Templator(package_name)
        self.assertTrue(instance.package_name, package_name)

    def test_get_template_path_returns(self):
        """Test get_template_path return path."""
        package_name = 'hardest'
        instance = Templator(package_name)
        template_path = 'templates/tox.ini.jn2'
        full_tox_dir = instance.get_template_path(template_path)
        self.assertTrue(full_tox_dir.endswith(template_path))

    def test_get_template_fails_package(self):
        """Test get_template_path fails."""
        package_name = 'strange package name'
        instance = Templator(package_name)
        template_path = 'templates/tox.ini.jn2'
        with self.assertRaises(TemplateNotFoundException):
            instance.get_template_path(template_path)

    def test_method_fails_template(self):
        """Fails with wrong template."""
        package_name = 'hardest'
        instance = Templator(package_name)
        template_path = 'templates/NOTEXIST.jn2'
        with self.assertRaises(TemplateNotFoundException):
            instance.get_template_path(template_path)

    def test_render(self):
        """Test render method."""
        package_name = 'hardest'
        instance = Templator(package_name)
        first = ''.join(random.sample(string.ascii_letters, 15))
        second = ''.join(random.sample(string.ascii_letters, 15))
        args = {'first': first, 'second': second}
        mock_path = 'hardest.templator.Templator.get_template_path'
        with mock.patch(mock_path) as patch:
            file_path = 'tests/fixtures/template.jn2'
            patch.return_value = file_path
            content = instance.render(file_path, **args)
            self.assertEqual('start{}end|start{}end'.format(first, second),
                             content)
