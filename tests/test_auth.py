from ebooks.auth import is_safe_url, load_saml_settings, prepare_flask_request
from unittest.mock import patch

import os

from flask import request


def test_is_safe_url_is_safe(app):
    with app.test_request_context():
        x = is_safe_url('http://localhost/?safe')
        assert x is True


def test_is_safe_url_is_not_safe(app):
    with app.test_request_context():
        x = is_safe_url('//unsafe-site.com')
        assert x is False


@patch.dict(os.environ, {
    'SP_ENTITY_ID': 'http://ebooks.test/shibboleth/',
    'SP_ACS_URL': 'http://ebooks.test/shibboleth/?acs',
    'SP_SLS_URL': 'http://ebooks.test/shibboleth/?sls',
    'IDP_ENTITY_ID': 'https://test-idp.com/saml2/metadata/',
    'IDP_SSO_URL': 'https://test-idp.com/saml2/http-post/sso/',
    'IDP_SLS_URL': 'http://test-idp.com/saml2/http-post/slo/',
    'SP_CERT': 'iamacert',
    'SP_KEY': 'iamasecretkey',
    'IDP_CERT': 'iamacert'})
def test_load_saml_settings_returns_json(app):
    with app.test_request_context():
        x = load_saml_settings()
        assert x['sp']['entityId'] == 'http://ebooks.test/shibboleth/'


@patch.dict(os.environ, {'SP_ENTITY_ID': ''})
def test_load_saml_settings_missing_env_variable_raises_exception(app):
    # TODO: raise an exception if there is a missing SAML env variable. We know
    # that this will break auth, so the app shouldn't run without it.
    pass


def test_prepare_flask_request(app):
    with app.test_request_context():
        x = prepare_flask_request(request)
        assert x['http_host'] == 'localhost'
