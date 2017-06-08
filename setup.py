#!/usr/bin/python3

# ~/dev/py/clp/setup.py

import re
from distutils.core import setup
__version__ = re.search(r"__version__\s*=\s*'(.*)'",
                        open('src/clp/__init__.py').read()).group(1)

# see http://docs.python.org/distutils/setupscript.html

with open('README.rst', 'r') as file:
    LONG_DESC = file.read()

setup(name='clp',
      version=__version__,
      author='Jim Dixon',
      author_email='jddixon@gmail.com',
      #
      # wherever we have a .py file that will be imported, we
      # list it here, without the extension but SQuoted
      py_modules=[],
      #
      # a package has a subdir and an __init__.py
      packages=['src/clp', ],
      #
      # following could be in scripts/ subdir; SQuote
      scripts=[],
      #
      description='clp: utilities for Computer Language Processing',
      long_description=LONG_DESC,
      url='https://jddixon.github.io/clp',
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Programming Language :: Python 3',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],)
