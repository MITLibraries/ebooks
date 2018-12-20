from __future__ import absolute_import

from flask import Flask
from flask_sslify import SSLify
import os
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN') or None,
    integrations=[FlaskIntegration()]
)

app = Flask(__name__)
app.config['ALEPH_API_KEY'] = os.getenv('ALEPH_API_KEY')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
sslify = SSLify(app, permanent=True)

import ebooks.auth
import ebooks.queries
import ebooks.views
