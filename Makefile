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
	flake8 src/ tests/
	isort --recursive --check-only --diff src tests
	black --check src/ tests/

format:
	isort --recursive src tests
	black src/ tests/

clean:
	find . -name '*.pyc' -delete

release:
	pip install twine wheel
	rm -rf dist/*
	python setup.py sdist bdist_wheel
	twine upload -s dist/*
