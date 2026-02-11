# common make vars and targets:
export LINTER = flake8
export PYLINTFLAGS = --exclude=__main__.py

export CLOUD_MONGO = 0

PYTESTFLAGS = -vv --verbose --cov-branch --cov-report term-missing --tb=short -W ignore::FutureWarning

# Absolute path to the project root (directory containing this common.mk)
PROJECT_ROOT := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))

MAIL_METHOD = api

FORCE:

tests: lint pytests

lint: $(patsubst %.py,%.pylint,$(PYTHONFILES))

%.pylint:
	$(LINTER) $(PYLINTFLAGS) $*.py

pytests: FORCE
	PYTHONPATH=$(PROJECT_ROOT) PYTEST_DISABLE_PLUGIN_AUTOLOAD= pytest $(PYTESTFLAGS) --cov=$(PKG)

# test a python file:
%.py: FORCE
	$(LINTER) $(PYLINTFLAGS) $@
	PYTHONPATH=$(PROJECT_ROOT) PYTEST_DISABLE_PLUGIN_AUTOLOAD= pytest $(PYTESTFLAGS) tests/test_$*.py

nocrud:
	-rm *~
	-rm *.log
	-rm *.out
	-rm .*swp
	-rm $(TESTDIR)/*~
