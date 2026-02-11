include common.mk

# Our directories
CITIES_DIR = cities
DB_DIR = data
SEC_DIR = security
REQ_DIR = .
# SEC_DIR = security
SERVER_DIR = server



FORCE:

prod: all_tests

github: FORCE
	- git commit -a
	git push origin master

all_tests: FORCE
	@echo "Running all tests from repo root..."
	@PYTHONPATH=. PYTEST_DISABLE_PLUGIN_AUTOLOAD= \
	python -m pytest -vv \
		USstates/tests \
		cities/tests \
		data/tests \
		examples/tests \
		security/tests \
		server/tests \
		testing \
		-p no:langsmith -p pytest_cov \
		--tb=short -W ignore::FutureWarning

dev_env: FORCE
	pip install -r $(REQ_DIR)/requirements-dev.txt
	@echo "You should set PYTHONPATH to: "
	@echo $(shell pwd)

prod_env: FORCE
	pip install -r $(REQ_DIR)/requirements.txt


docs: FORCE
	cd $(API_DIR); make docs
