import json
import pytest
import requests.exceptions
import requests_mock
from netaddr import IPNetwork

from wsgi_aws_unproxy import UnProxy


@pytest.fixture
def wsgi_app():
    def app(environ, start_response):
        return "ip={}, ff={}".format(
            environ['REMOTE_ADDR'], environ.get('HTTP_X_FORWARDED_FOR', '')
        )

    json_data = """
    {
        "syncToken": "1490372531",
        "createDate": "2017-03-24-16-22-11",
        "prefixes": [
            {
                "ip_prefix": "13.32.0.0/15",
                "region": "GLOBAL",
                "service": "AMAZON"
            },
            {
                "ip_prefix": "13.54.0.0/15",
                "region": "ap-southeast-2",
                "service": "AMAZON"
            },
            {
                "ip_prefix": "13.32.0.0/15",
                "region": "GLOBAL",
                "service": "CLOUDFRONT"
            }
        ],
        "ipv6_prefixes": [
            {
                "ipv6_prefix": "2400:6500:0:7000::/56",
                "region": "ap-southeast-1",
                "service": "AMAZON"
            }
        ]
    }
    """

    with requests_mock.mock() as rm:
        rm.get(
            'https://ip-ranges.amazonaws.com/ip-ranges.json',
            text=json_data)
        app = UnProxy(app)

        yield app


def test_assert_networks(wsgi_app):
    """
    Test that wrapping wsgi object in unproxy doesn't crash.
    """
    assert wsgi_app.allowed_proxy_ips == [
        # Default
        IPNetwork('10.0.0.0/8'),
        IPNetwork('172.16.0.0/12'),
        IPNetwork('192.168.0.0/16'),

        # Extra
        IPNetwork("13.32.0.0/15"),
    ]

    assert not wsgi_app._is_proxy_ip('127.0.0.1')
    assert not wsgi_app._is_proxy_ip('FOOBAR')
    assert wsgi_app._is_proxy_ip('10.0.0.99')
    assert wsgi_app._is_proxy_ip('13.32.0.99')


def test_internal_ip(wsgi_app):
    """Should skip first proxy. """
    assert wsgi_app({
        'REMOTE_ADDR': '10.0.0.99',
        'HTTP_X_FORWARDED_FOR': '1.2.1.2, 172.20.46.123'
    }, None) == 'ip=1.2.1.2, ff='


def test_internal_invalid_ip(wsgi_app):
    """Should skip first proxy. """
    assert wsgi_app({
        'REMOTE_ADDR': '172.20.5.4',
        'HTTP_X_FORWARDED_FOR': '1.3.4.5, 172.20.46.123, 94.128.0.1, 172.20.45.1'
    }, None) == 'ip=94.128.0.1, ff=1.3.4.5, 172.20.46.123'


def test_cloudfront_ip(wsgi_app):
    """Should skip first proxy. """
    assert wsgi_app({
        'REMOTE_ADDR': '10.0.0.99',
        'HTTP_X_FORWARDED_FOR': '1.2.1.2, 13.32.0.99'
    }, None) == 'ip=1.2.1.2, ff='


def test_non_proxy_ip_multiple(wsgi_app):
    """Should return last (is not a proxy)."""
    assert wsgi_app({
        'REMOTE_ADDR': '10.0.0.99',
        'HTTP_X_FORWARDED_FOR': '1.2.1.2, 1.2.3.3'
    }, None) == 'ip=1.2.3.3, ff=1.2.1.2'


def test_proxy_ip(wsgi_app):
    """Remote addr is proxy, returns the forward."""
    assert wsgi_app({
        'REMOTE_ADDR': '10.0.0.99',
        'HTTP_X_FORWARDED_FOR': '11.22.33.44'
    }, None) == 'ip=11.22.33.44, ff='


def test_non_proxy_ip(wsgi_app):
    """Not a proxy. so REMOTE_ADDR remains unchanged."""
    assert wsgi_app({
        'REMOTE_ADDR': '88.88.88.88',
        'HTTP_X_FORWARDED_FOR': '11.22.33.44'
    }, None) == 'ip=88.88.88.88, ff=11.22.33.44'


def test_no_xforwarded_header(wsgi_app):
    """No X-Forwarded-For should not crash."""
    assert wsgi_app({
        'REMOTE_ADDR': '10.0.0.99'
    }, None) == 'ip=10.0.0.99, ff='


def test_unproxy_bad_request():
    """Test that wrapping wsgi object in unproxy doesn't crash"""
    def app(environ, start_response):
        return environ['REMOTE_ADDR']  # pragma: no cover

    with requests_mock.mock() as rm:
        rm.get('https://ip-ranges.amazonaws.com/ip-ranges.json',
               exc=requests.exceptions.ConnectTimeout)
        app = UnProxy(app)
        assert app.allowed_proxy_ips == []


def test_unproxy_bad_json():
    """Test that wrapping wsgi object in unproxy doesn't crash"""
    def app(environ, start_response):
        return environ['REMOTE_ADDR']  # pragma: no cover

    with requests_mock.mock() as rm:
        rm.get('https://ip-ranges.amazonaws.com/ip-ranges.json', text='{NOT_JSON!}')
        app = UnProxy(app)
        assert app.allowed_proxy_ips == []
