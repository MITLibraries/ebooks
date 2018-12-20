from ebooks import app

import json
import os

from flask import redirect, request, session, url_for
from functools import wraps
from urllib.parse import urljoin, urlparse


def load_saml_settings():
    json_settings = {}
    with open("saml/settings.json", 'r') as json_file:
        json_settings = json.load(json_file)
        json_settings['debug'] = app.config['DEBUG']
        json_settings['sp']['entityId'] = os.getenv('SP_ENTITY_ID')
        json_settings['sp']['assertionConsumerService']['url'] = \
            os.getenv('SP_ACS_URL')
        json_settings['sp']['x509cert'] = os.getenv('SP_CERT')
        json_settings['sp']['privateKey'] = os.getenv('SP_KEY')
        json_settings['idp']['entityId'] = os.getenv('IDP_ENTITY_ID')
        json_settings['idp']['singleSignOnService']['url'] = \
            os.getenv('IDP_SSO_URL')
        json_settings['idp']['x509cert'] = os.getenv('IDP_CERT')
    return json_settings


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'samlSessionIndex' not in session:
            return redirect(url_for('saml', sso=True, next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def prepare_flask_request(request):
    url_data = urlparse(request.url)
    return {
        'https': 'on' if request.scheme == 'https' else 'off',
        'http_host': request.host,
        'server_port': url_data.port,
        'script_name': request.path,
        'get_data': request.args.copy(),
        'post_data': request.form.copy()
    }
