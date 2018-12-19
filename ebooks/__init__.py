from __future__ import absolute_import

from flask import Flask
from flask_sslify import SSLify
import os

app = Flask(__name__)
app.config['ALEPH_API_KEY'] = os.getenv('ALEPH_API_KEY')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
sslify = SSLify(app, permanent=True)

import ebooks.auth
import ebooks.queries
import ebooks.views
