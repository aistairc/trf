#!/usr/bin/env python

from setuptools import setup, find_packages


setup(name='trf',
      version='0.1',
      description='A tool to calculate text readability features',
      author='Akihiko Watanabe',
      author_email='watanabe@lr.pi.titech.ac.jp',
      url='https://github.com/aistairc/trf',
      packages=find_packages(),
      install_requires=[
          "numpy",
          "six"
      ],
      entry_points={"console_scripts": ["trf = trf.cmdline:main"]})
