.PHONY: all lint flake8 tests setup

ifeq ($(OS),Windows_NT)
PYTHON = venv/Scripts/python.exe
COVERAGE = venv/Scripts/coverage.exe
PTEST = venv/Scripts/pytest.exe
else
PYTHON = ./venv/bin/python
COVERAGE = ./venv/bin/coverage
PTEST = ./venv/bin/pytest
endif

SOURCE = tester_alice_skill_flask
TESTS = tests

PYLINT = $(PYTHON) -m pylint
PYLINT2 = $(PYLINT) --rcfile .pylintrc2
FLAKE8 = $(PYTHON) -m flake8
PEP257 = $(PYTHON) -m pep257
PYTEST = $(PTEST) --cov=$(SOURCE) --cov-report term:skip-covered
PIP = $(PYTHON) -m pip install

all: tests

flake8:
	$(FLAKE8) $(SOURCE)
	$(FLAKE8) $(TESTS)/test

lint:
	$(PYLINT) $(TESTS)/test
	$(PYLINT) $(SOURCE)

lint2:
	$(PYLINT2) $(TESTS)/test
	$(PYLINT2) $(SOURCE)

pep257:
	$(PEP257) --match='.*\.py' $(TESTS)/test
	$(PEP257) $(SOURCE)

tests2: flake8 pep257 lint2
	$(PYTEST) --durations=5 $(TESTS)
	$(COVERAGE) html --skip-covered

tests: flake8 pep257 lint
	$(PYTEST) --durations=5 $(TESTS)
	$(COVERAGE) html --skip-covered

package:
	$(PYTHON) -m build -n

pypitest: package
	$(PYTHON) -m twine upload --config-file .pypirc --repository testpypi dist/*

pypi: package
	$(PYTHON) -m twine upload --config-file .pypirc dist/*

setup: setup_python setup_pip

setup2: setup_python2 setup_pip2

setup_pip:
	$(PIP) --upgrade pip
	$(PIP) -r requirements.txt
	$(PIP) -r deploy.txt
	$(PIP) -r $(TESTS)/requirements.txt

setup_pip2:
	$(PIP) --upgrade pip
	$(PIP) -r requirements2.txt
	$(PIP) -r $(TESTS)/requirements.txt

setup_python:
	$(PYTHON_BIN) -m venv ./venv

setup_python2:
	$(PYTHON_BIN) -m pip install virtualenv
	$(PYTHON_BIN) -m virtualenv ./venv
