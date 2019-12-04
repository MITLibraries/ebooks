import requests

from ebooks import app
from ebooks.auth import (is_safe_url, load_saml_settings, login_required,
                         prepare_flask_request)
from ebooks.queries import get_filenames, get_metadata, get_url, get_volumes
from flask import (abort, make_response, redirect, render_template, request,
                   send_file, session)
from onelogin.saml2.auth import OneLogin_Saml2_Auth

saml_settings = load_saml_settings()


@app.route('/saml/', methods=['GET', 'POST'])
def saml():
    req = prepare_flask_request(request)
    auth = OneLogin_Saml2_Auth(req, saml_settings)
    errors = []
    next_page = request.args.get('next')
    if not next_page or is_safe_url(next_page) is False:
        next_page = ''

    if 'sso' in request.args:
        return redirect(auth.login(return_to=next_page))

    elif 'acs' in request.args:
        auth.process_response()
        errors = auth.get_errors()
        if not auth.is_authenticated():
            # TODO: return something helpful to the user
            pass
        if len(errors) == 0:
            session['samlNameId'] = auth.get_nameid()
            session['samlSessionIndex'] = auth.get_session_index()
            return redirect(request.form['RelayState'])
        else:
            print('Errors: %s', errors)
            print('Last error reason: %s', auth.get_last_error_reason())


@app.route('/saml/metadata/')
def metadata():
    req = prepare_flask_request(request)
    auth = OneLogin_Saml2_Auth(req, saml_settings)
    settings = auth.get_settings()
    metadata = settings.get_sp_metadata()
    errors = settings.validate_metadata(metadata)

    if len(errors) == 0:
        resp = make_response(metadata, 200)
        resp.headers['Content-Type'] = 'text/xml'
    else:
        resp = make_response(', '.join(errors), 500)
    return resp


@app.route("/item/<item>")
@login_required
def item(item="None"):
    metadata = {}
    files = []
    try:
        record = requests.get("https://library.mit.edu/rest-dlf/record/mit01" +
                              item + "?view=full&key=" +
                              app.config['ALEPH_API_KEY'])
        marc_xml = record.content
        metadata = get_metadata(marc_xml)
    except AttributeError:
            metadata['Error'] = 'Item not found.'
    try:
        filenames = get_filenames(item)
        for f in filenames:
            files.append({'name': f, 'url': get_url(f)})
    except KeyError:
        pass

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


# @app.route('/docs/<filename>')
# @login_required
# def file(filename):
#     if '..' in filename or filename.startswith('/'):
#         abort(404)
#     obj = get_file(filename)
#     if obj == 404:
#         abort(404)
#     else:
#         return send_file(obj['Body'], mimetype=obj['ContentType'])
