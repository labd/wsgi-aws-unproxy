#!/usr/bin/env python
import re
from setuptools import setup

install_require = [
    'netaddr>=0.7.19',
    'requests>=2.23.0',
]

docs_require = [
    'sphinx>=1.4.0',
]

tests_require = [
    "coverage[toml]>=7.6",
    "requests-mock>=1.12",
    "pytest-cov>=6.0",
    "pytest>=8.3",
    # Linting
    "ruff",
]


with open('README.rst') as fh:
    long_description = re.sub('^.. start-no-pypi.*^.. end-no-pypi', '',
                              fh.read(), flags=re.M | re.S)


setup(
    name='wsgi-aws-unproxy',
    version='1.2.1',
    description="Simple wsgi middleware to unproxy AWS",
    long_description=long_description,
    url='https://github.com/labd/wsgi-aws-unproxy',
    author="Lab Digital",
    author_email="opensource@labdigital.nl",
    python_requires=">=3.11",
    install_requires=install_require,
    tests_require=tests_require,
    extras_require={
        'docs': docs_require,
        'test': tests_require,
    },
    package_dir={'': 'src'},
    py_modules=['wsgi_aws_unproxy'],
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    zip_safe=False,
)
