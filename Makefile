.PHONY: install clean test retest coverage

install:
	pip install -e .[docs,test]

test:
	py.test -vvv

retest:
	py.test -vvv --lf

coverage:
	py.test --cov=wsgi_aws_unproxy --cov-report=term-missing --cov-report=html

lint:
	ruff format --check src tests
	ruff check src tests

format:
	ruff format src tests
	ruff check --fix src tests

clean:
	find . -name '*.pyc' -delete

release:
	pip install twine wheel
	rm -rf dist/*
	python setup.py sdist bdist_wheel
	twine upload -s dist/*
