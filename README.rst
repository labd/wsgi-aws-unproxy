.. start-no-pypi

.. image:: https://github.com/labd/wsgi-aws-unproxy/workflows/Python%20Tests/badge.svg
    :target: https://github.com/labd/wsgi-aws-unproxy/actions
    
.. image:: http://codecov.io/github/LabD/wsgi-aws-unproxy/coverage.svg?branch=master
    :target: http://codecov.io/github/LabD/wsgi-aws-unproxy?branch=master

.. image:: https://img.shields.io/pypi/l/wsgi-aws-unproxy.svg
    :target: https://pypi.python.org/pypi/wsgi-aws-unproxy/

.. image:: https://img.shields.io/pypi/v/wsgi-aws-unproxy.svg
    :target: https://pypi.python.org/pypi/wsgi-aws-unproxy/

.. end-no-pypi


================
WSGI AWS Unproxy
================

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
