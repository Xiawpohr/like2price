PKG=like2price
VERSION := $(shell cat VERSION.txt)

.PHONY: version init flake8 pylint lint test coverage clean

version:
	echo $(VERSION)

init: clean
	pipenv install --dev

flake8:
	pipenv run flake8 $(PKG)

pylint:
	pipenv run pylint $(PKG) --ignore=tests

lint: flake8 pylint