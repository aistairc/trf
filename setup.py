#!/usr/bin/env python

from pip.req import parse_requirements
from setuptools import setup, find_packages

install_reqs = parse_requirements('requirements.txt', session='hack')

setup(name='trf',
      version='0.1',
      description='A tool to calculate text readability features',
      author='Akihiko Watanabe, Soichiro Murakami, and Akira Miyazawa',
      author_email='{watanabe, murakami}@lr.pi.titech.ac.jp, miyazawa-a@nii.ac.jp',
      url='https://github.com/aistairc/trf',
      packages=find_packages("trf"),
      install_requires=install_reqs)
#      package_data={'', ['']},
