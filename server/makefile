.PHONY: tests pytests flake

tests: pytests

pytests:
	@PYTHONPATH=.. PYTEST_DISABLE_PLUGIN_AUTOLOAD= \
	python -m pytest -vv tests \
	-p no:langsmith -p pytest_cov \
	--cov=server --cov-branch --cov-report=term-missing \
	--tb=short -W ignore::FutureWarning

flake:
	flake8 --exclude=__main__.py __init__.py endpoints.py