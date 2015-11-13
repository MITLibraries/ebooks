#!/usr/bin/python

import logging, os, sys

activate_this = '/var/www/libraries-test.mit.edu/htdocs/secure/ebooks/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

sys.path.insert(0, '/var/www/libraries-test.mit.edu/htdocs/secure/ebooks')
os.chdir('/var/www/libraries-test.mit.edu/htdocs/secure/ebooks')

logging.basicConfig(stream=sys.stderr)

from ebooks import app as application
