"""Templator class which helps render templates."""
from typing import List  # noqa pylint: disable=unused-import
from typing import Optional  # noqa pylint: disable=unused-import

import pkg_resources

from jinja2 import Template


class Templator(object):
    """Template generator."""

    def __init__(self, package_name):
        """Init constructor."""
        # type: (str) -> None
        self.package_name = package_name

    def render(self, template_name, **kwargs):
        """Render by template_name."""
        # type: (str, Optional[Dict[str]]) -> str

        full_path = self.get_template_path(template_name)

        file_handler = open(full_path)
        file_handler.close()
        template_content = str(file_handler.read())

        template = Template(template_content)
        rendered = str(template.render(**kwargs))
        return rendered

    def get_template_path(self, template_name):
        """Get template path."""
        # type: (str) -> str
        return pkg_resources.resource_filename(self.package_name,
                                               template_name)
