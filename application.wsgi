#!/usr/bin/python

import logging, sys

sys.path.insert(0, '/var/www/ebooks')

logging.basicConfig(stream=sys.stderr)

from app import app as application