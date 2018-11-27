from flask import (abort, redirect, render_template,
                   request, send_file, url_for)
from flask_login import (current_user, login_required,
                         login_user, LoginManager, logout_user, UserMixin)

from werkzeug.urls import url_parse

import os
import requests

from ebooks import app
from ebooks.queries import get_file, get_filenames, get_metadata, get_volumes

ALEPH_API_KEY = os.getenv('ALEPH_API_KEY')
login = LoginManager(app)
login.login_view = 'login'


# Define the login route function here
@app.route("/login")
def login():
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
        next_page = url_for('index')
    if current_user.is_authenticated:
        return redirect(next_page)
    # Log in user here and redirect to next_page
    # Call authenticate function
    # Create user variable that is instance of User class, with results of
    #       authenticate function?
    # Call login_user(user)
    return("Login process to be implemented")


@app.route("/")
@app.route("/<item>")
# @login_required
def index(item="002341336"):
    files = get_filenames(item)

    metadata = {}
    try:
        record = requests.get("https://library.mit.edu/rest-dlf/record/mit01" +
                              item + "?view=full&key=" + ALEPH_API_KEY)
        marc_xml = record.content
        metadata = get_metadata(marc_xml)
    except:
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
