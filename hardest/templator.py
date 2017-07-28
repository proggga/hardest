"""Templator class which helps render templates."""
from typing import List  # noqa pylint: disable=unused-import
from typing import Optional  # noqa pylint: disable=unused-import

import pkg_resources

from jinja2 import Template

from hardest.exceptions import TemplateNotFoundException


class Templator(object):
    """Template generator."""

    def __init__(self, package_name):
        """Init constructor."""
        # type: (str) -> None
        self.package_name = package_name

    def render(self, template_name, **kwargs):  # pragma: nocover
        """Render by template_name."""
        # type: (str, Optional[Dict[str]]) -> str

        full_path = self.get_template_path(template_name)

        file_handler = open(full_path)
        template_content = str(file_handler.read())
        file_handler.close()

        template = Template(template_content)
        rendered_content = str(template.render(**kwargs))
        return rendered_content

    def get_template_path(self, template_name):
        """Get template path."""
        # type: (str) -> str
        try:
            if pkg_resources.resource_exists(self.package_name,
                                             template_name):
                return pkg_resources.resource_filename(self.package_name,
                                                       template_name)
        except ImportError:
            message = ('Package "{}" not found'
                       .format(self.package_name))
            raise TemplateNotFoundException(message)
        else:
            message = ('Template "{}" not found in package "{}"'
                       .format(template_name, self.package_name))
            raise TemplateNotFoundException(message)
