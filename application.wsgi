#!/usr/bin/python

import logging, sys

sys.path.insert(0, '/var/www/libraries-test.mit.edu/htdocs/secure/ebooks')

logging.basicConfig(stream=sys.stderr)

from app import app as application
