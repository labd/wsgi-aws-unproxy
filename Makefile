.PHONY: install clean test retest coverage lint format

install:
	uv sync

test:
	uv run pytest -vvv

retest:
	uv run pytest -vvv --lf

coverage:
	uv run pytest --cov=wsgi_aws_unproxy --cov-report=term-missing --cov-report=html

lint:
	uv run ruff format --check src tests
	uv run ruff check src tests

format:
	uv run ruff format src tests
	uv run ruff check --fix src tests

clean:
	find . -name '*.pyc' -delete
