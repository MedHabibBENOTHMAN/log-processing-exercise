.PHONY: help install run test lint format typecheck check clean

help:  ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

install:  ## Sync dev dependencies via uv
	uv sync --group dev

run:  ## Run the script against data.log
	uv run python process_log.py data.log

test:  ## Run the test suite
	uv run pytest

lint:  ## Lint with ruff
	uv run ruff check .

format:  ## Format with ruff
	uv run ruff format .

typecheck:  ## Static type check with mypy strict
	uv run mypy .

check: lint typecheck test  ## Run lint + typecheck + tests (CI gate)

clean:  ## Remove caches and venv
	rm -rf .venv .pytest_cache .mypy_cache .ruff_cache __pycache__ tests/__pycache__
