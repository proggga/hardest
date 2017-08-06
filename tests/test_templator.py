"""Test templator class."""
import unittest


class TemplatorTestCase(unittest.TestCase):
    """Templator test case."""

    def setUp(self):
        """Set Up."""
        self.package_name = 'hardest'
        self.template_path = 'templates/tox.ini.jn2'

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

        full_tox_dir = instance.get_template_path(self.template_path)
        self.assertTrue(full_tox_dir.endswith(self.template_path))

    def test_get_template_fails_package(self):
        """Test get_template_path fails."""
        import hardest
        import hardest.exceptions

        package_name = 'strange package name'
        instance = hardest.Templator(package_name)
        with self.assertRaises(hardest.exceptions.TemplateNotFoundException):
            instance.get_template_path(self.template_path)

    def test_method_fails_template(self):
        """Fails with wrong template."""
        import hardest
        import hardest.exceptions

        instance = hardest.Templator(self.package_name)
        template_path = 'NOTEXIST.jn2'
        with self.assertRaises(hardest.exceptions.TemplateNotFoundException):
            instance.get_template_path(template_path)

    def test_get_template(self):
        """Test get template instance."""
        import hardest
        instance = hardest.Templator(self.package_name)
        context = {'first': 'a', 'second': 'b'}
        template = instance.get_template(self.template_path, context)
        self.assertIsInstance(template, hardest.Template)

    def test_get_template_no_context(self):
        """Test get template instance without context."""
        import hardest
        instance = hardest.Templator(self.package_name)
        template = instance.get_template(self.template_path)
        self.assertIsInstance(template, hardest.Template)

    def test_get_template_no_exists(self):
        """Test get template instance without context."""
        import hardest
        import hardest.exceptions

        instance = hardest.Templator(self.package_name)
        template_path = 'NOTEXIST.jn2'
        with self.assertRaises(hardest.exceptions.TemplateNotFoundException):
            instance.get_template(template_path)
