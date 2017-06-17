#!/usr/bin/env python
"""Setup project"""

from setuptools import setup

setup(name='hardest',
      version='0.0.1a',
      description='Hardcore testing tool',
      author='Mikhail Fesenko',
      author_email='proggga@gmail.com',
      packages=['hardest'],
      entry_points={
          'console_scripts': [
              'hardest = hardest.command_line:main',
          ],
      })
