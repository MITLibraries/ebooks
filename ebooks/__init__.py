from __future__ import absolute_import

from flask import Flask

import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

import ebooks.queries
import ebooks.views
