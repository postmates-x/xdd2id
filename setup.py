#!/usr/bin/env python

import re
from setuptools import setup


_version = re.search(r'__version__\s+=\s+\'(.*)\'',
                     open('xdd2id/__init__.py').read()).group(1)


setup(name='xdd2id',
      version=_version,
      packages=['xdd2id'],
      description='CANopen XML dictionary to Ingenia dictionary converter',
      long_description=open('README.rst').read(),
      author='Ingenia Motion Control',
      author_email='support@ingeniamc.com',
      url='https://www.ingeniamc.com',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Topic :: Software Development :: Libraries'
      ],
      entry_points={
          'console_scripts': ['xdd2id = xdd2id.__main__:main']
      })
