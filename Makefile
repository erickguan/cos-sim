.PHONY: update-dependencies
update-dependencies:
	uv pip compile requirements.in > requirements.txt
	uv pip compile requirements-dev.in > requirements-dev.txt

.PHONY: lint
lint:
	ruff check .
	ruff format --check .

.PHONY: lint-fix
lint-fix:
	ruff check --fix .
	ruff format .

.PHONY: test
test:
	PYTHONPATH=. pytest . -vv
