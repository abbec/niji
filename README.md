
[![Build Status](https://travis-ci.org/abbec/niji.svg)](https://travis-ci.org/abbec/niji)
[![Code Health](https://landscape.io/github/abbec/niji/master/landscape.svg?style=flat)](https://landscape.io/github/abbec/niji/master)
[![Coverage Status](https://coveralls.io/repos/abbec/niji/badge.svg)](https://coveralls.io/r/abbec/niji)
[![Documentation Status](https://readthedocs.org/projects/niji/badge/?version=latest)](https://readthedocs.org/projects/niji/?badge=latest)

# niji
A small, simple package management library written in Python. Supports Python 2.7+ and Python 3.4+.

## setting up for development

create a virtualenv and run

	$ pip install -r requirements.txt

This will install all the needed python packages.

Set the package up for development

	$ pip install -e .

This will create an editable install of the package which is needed for tests and other things.

To run tests

	$ py.test

or to run with different python versions at once (you will need python 2.7, python 3.4 and pypy installed):

	$ tox

Happy hacking!
