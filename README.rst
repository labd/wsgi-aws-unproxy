================
WSGI AWS Unproxy
================

Set the correct REMOTE_ADDR based on the X-Forwarded-For header while only
trusting the CloudFront IP addresses.


Getting started
===============

Using this module is really simple.  In Django for example edit the wsgi.py
file and add the following to the end of the file.

.. code-block:: python

  from wsgi_aws_unproxy import UnProxy
  application = UnProxy(application)


Installation
============

You can install the latest version using pip::

    pip install wsgi-aws-unproxy
