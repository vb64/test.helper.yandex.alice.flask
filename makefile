.PHONY: all setup flake8 lint

ifeq ($(OS),Windows_NT)
PYTHON = venv\Scripts\python.exe
else
PYTHON = ./venv/bin/python
endif

SOURCE = tester_alice_skill_flask
COVERAGE = $(PYTHON) -m coverage

all: tests

flake8:
	$(PYTHON) -m flake8 --max-line-length=110 $(SOURCE)

lint:
	$(PYTHON) -m pylint $(SOURCE)

coverage:
	$(COVERAGE) run tests/test_buy_elephant.py

html:
	$(COVERAGE) html --skip-covered

tests: flake8 lint coverage html
	$(COVERAGE) report --skip-covered

dist:
	$(PYTHON) setup.py sdist bdist_wheel

upload_piptest: tests dist
	$(PYTHON) -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

upload_pip: tests dist
	$(PYTHON) -m twine upload dist/*

setup: setup_python setup_pip

setup_pip:
	$(PYTHON) -m pip install -r requirements.txt
	$(PYTHON) -m pip install -r tests/requirements.txt

setup_python:
	python -m virtualenv venv
