from __future__ import absolute_import

import ebooks
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
