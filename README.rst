================
WSGI AWS Unproxy
================

.. image:: https://img.shields.io/pypi/v/wsgi-aws-unproxy
    :target: https://pypi.org/project/wsgi-aws-unproxy/
    :alt: PyPI

.. image:: https://github.com/labd/wsgi-aws-unproxy/actions/workflows/python-test.yml/badge.svg
    :target: https://github.com/labd/wsgi-aws-unproxy/actions/workflows/python-test.yml
    :alt: Python Tests

.. image:: https://img.shields.io/pypi/l/wsgi-aws-unproxy
    :target: https://pypi.org/project/wsgi-aws-unproxy/
    :alt: License

Set the correct ``REMOTE_ADDR`` based on the ``X-Forwarded-For`` header,
while only trusting the CloudFront IP addresses.

This module is applied as WSGI middleware, fixing the IP-address retrieval for the entire application in a secure manner.
As extra benefit, external packages no longer have to write abstraction layers to retrieve the IP-address header.


Django example
==============

In Django edit the ``wsgi.py`` file to apply the module:

.. code-block:: python

    from django.core.wsgi import get_wsgi_application
    from wsgi_aws_unproxy import UnProxy

    application = get_wsgi_application()
    application = UnProxy(application)

Now all packages can just read ``request.META['REMOTE_ADDR']`` to fetch the correct IP.
This includes contact forms, Sentry error reporting and rate limiting tools.


Installation
============

You can install the latest version using pip:

.. code-block:: bash

    pip install wsgi-aws-unproxy

And apply it as WSGI middleware:

.. code-block:: python

    from wsgi_aws_unproxy import UnProxy

    application = UnProxy(application)

Releasing
=========

Releases are managed with `changie <https://changie.dev>`_:

1. Add a changelog entry to your pull request with ``changie new``.
2. After merging to ``master``, a release pull request is opened (or updated)
   automatically, with the new version and the updated ``CHANGELOG.md``.
3. Merging the release pull request creates the GitHub release, which publishes
   the package to PyPI.
