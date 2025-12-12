include common.mk

# Our directories
CITIES_DIR = cities
DB_DIR = data
SEC_DIR = security
REQ_DIR = .
# SEC_DIR = security
SERVER_DIR = server

VENV = .venv
PYTHON = python3
PIP = $(VENV)/bin/pip


FORCE:

prod: all_tests

github: FORCE
	- git commit -a
	git push origin master

all_tests: FORCE
	cd $(CITIES_DIR); make tests
	cd $(SEC_DIR); make tests
	cd $(SERVER_DIR); make tests

dev_env: FORCE
	$(PYTHON) -m venv $(VENV)
# 	pip install -r $(REQ_DIR)/requirements-dev.txt
	$(PIP) install -r $(REQ_DIR)/requirements-dev.txt
# 	@echo "You should set PYTHONPATH to: "
# 	@echo $(shell pwd)
	@echo ""
	@echo "Dev env ready."
	@echo "Now run: source $(VENV)/bin/activate"
	@echo ""

docs: FORCE
	cd $(API_DIR); make docs
