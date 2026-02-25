# frontend/Makefile

NPM ?= npm
DEPS_STAMP := .deps.stamp

.PHONY: FORCE \
	prod check ci \
	all_checks all_tests \
	dev_env env install \
	start test lint build clean

FORCE:

# Install deps once (re-run only when package files change)
$(DEPS_STAMP): package.json package-lock.json
	$(NPM) ci
	@touch $(DEPS_STAMP)

install: $(DEPS_STAMP)
dev_env: install
env: install

start: install
	$(NPM) start

# non-interactive tests for CI/grading
test: install
	@echo "Running frontend tests..."
	CI=true $(NPM) test -- --watchAll=false --coverage

# CRA doesn't define "lint" in package.json, so run eslint directly
lint: install
	@echo "Running frontend lint..."
	npx eslint --ext .js,.jsx src --max-warnings=0

build: install
	@echo "Building frontend..."
	$(NPM) run build

# Back-end style aliases
all_tests: test
all_checks: lint test

# Common CI target name
check: all_checks
ci: prod

# Main grading target
prod: all_checks build

clean:
	rm -rf node_modules build $(DEPS_STAMP)
