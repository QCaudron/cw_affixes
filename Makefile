.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'


.PHONY: lint
lint:  ## Check code for style, imports, type hints, and docstring coverage.
	poetry run flake8 --exclude .venv,__init__.py . 
	poetry run black . --check --diff --quiet
	poetry run isort . --check
	poetry run mypy .


.PHONY: format
format:  ## Format with black, fix imports with isort, and remove unused imports with autoflake.
	poetry run black . --quiet
	poetry run isort .


.PHONY: ngrams
ngrams:  ## Generate n-grams.
	poetry run python generate_all_ngram_files.py


.DEFAULT_GOAL := help
