.PHONY: format lint build test

format:
	python3 scripts/format_repo.py

lint:
	python3 scripts/validate_repo.py

build:
	python3 scripts/validate_repo.py --quiet

test:
	python3 scripts/test_repo.py
