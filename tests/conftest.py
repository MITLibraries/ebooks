from __future__ import absolute_import

import ebooks
import os
import pytest
from webtest import TestApp


@pytest.yield_fixture
def app():
    app = ebooks.app
    ctx = app.test_request_context()
    ctx.push()
    yield app
    ctx.pop()


@pytest.fixture
def testapp(app):
    return TestApp(app)


@pytest.fixture
def record():
    with open(_fixtures('fake_record.xml')) as f:
        record = f.read()
        return record


def _fixtures(path):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(current_dir, 'fixtures', path)
