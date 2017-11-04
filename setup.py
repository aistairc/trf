#!/usr/bin/env python

from setuptools import setup, find_packages


setup(name='trf',
      version='0.1',
      description='A tool to calculate text readability features',
      author='Akihiko Watanabe, Soichiro Murakami, and Akira Miyazawa',
      author_email='{watanabe, murakami}@lr.pi.titech.ac.jp, miyazawa-a@nii.ac.jp',
      url='https://github.com/aistairc/trf',
      packages=find_packages("trf"),
      install_requires=[
          "numpy",
          "janome",
          "sqlalchemy"
      ],
      entry_points={"console_scripts": ["trf = trf.cmdline:main"]})
#      package_data={'', ['']},
