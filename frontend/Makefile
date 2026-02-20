# frontend/Makefile

FORCE:

# Main grading target
prod: all_checks build

# Run lint + tests (similar to backend all_tests)
all_checks: FORCE lint test

dev_env: FORCE
	npm ci

env: FORCE
	npm install

start: FORCE
	npm start

# non-interactive tests for CI/grading
test: FORCE
	@echo "Running frontend tests..."
	CI=true npm test -- --watchAll=false

lint: FORCE
	@echo "Running frontend lint..."
	CI=true npm run lint

build: FORCE
	@echo "Building frontend..."
	npm run build

clean: FORCE
	rm -rf node_modules build
