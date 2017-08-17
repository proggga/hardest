#!/usr/bin/env python
"""Setup project."""

from setuptools import setup  # type: ignore

setup(name='hardest',
      version='0.0.1',
      description='Hardcore testing tool',
      author='Mikhail Fesenko',
      author_email='proggga@gmail.com',
      zip_safe=False,
      packages=['hardest'],
      package_data={
          'hardest': [
              'templates/*.jn2',
          ]
      },
      entry_points={
          'console_scripts': [
              'hardest = hardest.command_line:main',
          ],
      })
