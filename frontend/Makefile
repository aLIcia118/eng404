# frontend/Makefile

NPM ?= npm
DEPS_STAMP := .deps.stamp

.PHONY: FORCE prod all_checks dev_env env start test lint build clean

FORCE:

# Install deps once (re-run only when package files change)
$(DEPS_STAMP): package.json package-lock.json
	$(NPM) ci
	@touch $(DEPS_STAMP)

dev_env: $(DEPS_STAMP)

env: $(DEPS_STAMP)

start: $(DEPS_STAMP)
	$(NPM) start

# non-interactive tests for CI/grading
test: $(DEPS_STAMP)
	@echo "Running frontend tests..."
	CI=true $(NPM) test -- --watchAll=false

# CRA doesn't define "lint" in package.json, so run eslint directly
lint: $(DEPS_STAMP)
	@echo "Running frontend lint..."
	./node_modules/.bin/eslint --ext .js,.jsx src --max-warnings=0

build: $(DEPS_STAMP)
	@echo "Building frontend..."
	$(NPM) run build

# Run lint + tests (similar to backend all_tests)
all_checks: lint test

# Main grading target
prod: all_checks build

clean:
	rm -rf node_modules build $(DEPS_STAMP)
