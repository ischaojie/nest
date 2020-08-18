#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command


here = os.path.abspath(os.path.dirname(__file__))

packages = ['nest']

requires = [
    'click', 'requests'

]

about = {}


with open(os.path.join(here, 'nest', '__version__.py'), 'r', encoding='utf-8') as f:
    exec(f.read(), about)
with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()
with open('HISTORY.md', 'r', encoding='utf-8') as f:
    history = f.read()


setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=readme,
    long_description_content_type='text/markdown',
    author=about['__author__'],
    author_email=about['__author_email__'],
    packages=packages,
    package_dir={'nest': 'nest'},
    package_data={'': ['LICENSE', 'NOTICE']},
    include_package_data=True,
    install_requires=requires,
    license=about['__license__'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],

    entry_points={
        'console_scripts': [
            'trans=nest:trans_cli',
            'wea=nest:wea_cli'
        ],
    },
)

# 'setup.py publish' shortcut.
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
    sys.exit()
