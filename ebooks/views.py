from ebooks import app
from ebooks.queries import get_file, get_filenames, get_metadata, get_volumes

from flask import (abort, make_response, redirect, render_template, request,
                   session, send_file, url_for)

from functools import wraps
from urllib.parse import urljoin, urlparse

from onelogin.saml2.auth import OneLogin_Saml2_Auth

import json
import os
import requests


json_settings = {}
with open("saml/settings.json", 'r') as json_file:
    json_settings = json.load(json_file)
    json_settings['debug'] = app.config['DEBUG']
    json_settings['sp']['entityId'] = os.getenv('SP_ENTITY_ID')
    json_settings['sp']['assertionConsumerService']['url'] = \
        os.getenv('SP_ACS_URL')
    json_settings['sp']['singleLogoutService']['url'] = os.getenv('SP_SLS_URL')
    json_settings['sp']['x509cert'] = os.getenv('SP_CERT')
    json_settings['sp']['privateKey'] = os.getenv('SP_KEY')
    json_settings['idp']['entityId'] = os.getenv('IDP_ENTITY_ID')
    json_settings['idp']['singleSignOnService']['url'] = \
        os.getenv('IDP_SSO_URL')
    json_settings['idp']['singleLogoutService']['url'] = \
        os.getenv('IDP_SLS_URL')
    json_settings['idp']['x509cert'] = os.getenv('IDP_CERT')


def init_saml_auth(req):
    auth = OneLogin_Saml2_Auth(req, json_settings)
    return auth


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'samlSessionIndex' not in session:
            return redirect(url_for('shibboleth', sso=True, next=request.url))
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


@app.route('/shibboleth/', methods=['GET', 'POST'])
def shibboleth():
    req = prepare_flask_request(request)
    auth = init_saml_auth(req)
    errors = []
    next_page = request.args.get('next')
    if not next_page or is_safe_url(next_page) is False:
        next_page = ''

    if 'sso' in request.args:
        return redirect(auth.login(return_to=next_page))

    elif 'slo' in request.args:
        name_id = None
        session_index = None
        if 'samlNameId' in session:
            name_id = session['samlNameId']
        if 'samlSessionIndex' in session:
            session_index = session['samlSessionIndex']
        return redirect(auth.logout(name_id=name_id,
                                    session_index=session_index))

    elif 'acs' in request.args:
        auth.process_response()
        errors = auth.get_errors()
        if not auth.is_authenticated():
            # TODO: return something helpful to the user
            pass
        if len(errors) == 0:
            session['samlUserdata'] = auth.get_attributes()
            session['samlNameId'] = auth.get_nameid()
            session['samlSessionIndex'] = auth.get_session_index()
            return redirect(request.form['RelayState'])
        else:
            print(errors)

    elif 'sls' in request.args:
        def dscb(): session.clear()
        url = auth.process_slo(delete_session_cb=dscb)
        errors = auth.get_errors()
        if len(errors) == 0:
            if url is not None:
                return redirect(url)
            else:
                # TODO: Do something useful here?
                return redirect('')


@app.route('/shibboleth/metadata/')
def metadata():
    req = prepare_flask_request(request)
    auth = init_saml_auth(req)
    settings = auth.get_settings()
    metadata = settings.get_sp_metadata()
    errors = settings.validate_metadata(metadata)

    if len(errors) == 0:
        resp = make_response(metadata, 200)
        resp.headers['Content-Type'] = 'text/xml'
    else:
        resp = make_response(', '.join(errors), 500)
    return resp


@app.route("/item/")
@app.route("/item/<item>")
@login_required
def item(item="002341336"):
    try:
        files = get_filenames(item)
        metadata = {}
        record = requests.get("https://library.mit.edu/rest-dlf/record/mit01" +
                              item + "?view=full&key=" +
                              app.config['ALEPH_API_KEY'])
        marc_xml = record.content
        metadata = get_metadata(marc_xml)
    except AttributeError:
            metadata['Error'] = 'Item not found.'

    fields = ['Title', 'Author', 'Edition', 'Publication', 'Series', 'ISBN',
              'ISSN', 'Original Version', 'Error']

    if 'Serial' in metadata:
        volumes = get_volumes(files)
        return render_template("serial.html", file_id=item, files=files,
                               metadata=metadata, fields=fields,
                               volumes=volumes)
    else:
        return render_template("landing.html", file_id=item, files=files,
                               metadata=metadata, fields=fields)


@app.route('/docs/<filename>')
@login_required
def file(filename):
    if '..' in filename or filename.startswith('/'):
        abort(404)
    obj = get_file(filename)
    if obj == 404:
        abort(404)
    else:
        return send_file(obj['Body'], mimetype=obj['ContentType'])
