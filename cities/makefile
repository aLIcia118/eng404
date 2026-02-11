.PHONY: tests pytests flake

PKG      := cities
TESTDIR  := tests

tests: pytests

pytests:
	@PYTHONPATH=.. PYTEST_DISABLE_PLUGIN_AUTOLOAD= \
	python -m pytest -vv $(TESTDIR) \
	-p no:langsmith -p pytest_cov \
	--cov=$(PKG) --cov-branch --cov-report=term-missing \
	--tb=short -W ignore::FutureWarning

flake:
	flake8 --exclude=__main__.py __init__.py queries.py