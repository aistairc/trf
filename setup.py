#!/usr/bin/env python

from pip._internal.req import parse_requirements
from setuptools import setup, find_packages

requirements = parse_requirements('requirements.txt', session='hack')

setup(name='trf',
      version='0.1',
      description='A tool to calculate text readability features',
      author='Akihiko Watanabe, Soichiro Murakami, and Akira Miyazawa',
      author_email='{watanabe, murakami}@lr.pi.titech.ac.jp, miyazawa-a@nii.ac.jp',
      url='https://github.com/aistairc/trf',
      packages=find_packages("trf"),
      install_requires=[str(requirement.req) for requirement in requirements])
