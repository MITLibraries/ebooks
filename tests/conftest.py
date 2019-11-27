import os

import boto3
from moto import mock_s3
import pytest
import requests_mock
from webtest import TestApp

import ebooks


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
def client(app):
    with app.test_client() as client:
        with client.session_transaction() as sess:
            sess['samlSessionIndex'] = 'exists'
        return client


@pytest.fixture
def s3_conn():
    with mock_s3():
        conn = boto3.resource('s3', region_name='us-1-east')
        conn.create_bucket(Bucket='samples')
        conn.Object('samples', 'sample_01-a.txt').put(Body='I am a file. I \
                live in a bucket.')
        conn.Object('samples', 'sample_01-b.txt').put(Body='I am a second \
                file. I also live in the bucket.')
        conn.Object('samples', 'has_volumes_a_2009.txt').put(Body='Vol 2009a')
        conn.Object('samples', 'has_volumes_b_2009.txt').put(Body='Vol 2009b')
        conn.Object('samples', 'sample.mp4').put(Body='fixtures/sample.mp4')
        yield conn


@pytest.fixture
def record():
    with open(_fixtures('sample.xml')) as f:
        record = f.read()
        return record


@pytest.fixture
def serial():
    with open(_fixtures('serial.xml')) as f:
        record = f.read()
        return record


@pytest.yield_fixture
def aleph(record, serial):
    with requests_mock.Mocker() as m:
        m.get('/rest-dlf/record/mit01sample',
              status_code=200, content=record.encode())
        m.get('/rest-dlf/record/mit01serial',
              status_code=200, content=serial.encode())
        m.get('/rest-dlf/record/mit01fake_item',
              status_code=200,
              content=('<?xmlversion = "1.0" encoding = ''"UTF-8"?>'
                       '<get-record><reply-text>Record does not exist'
                       '</reply-text><reply-code>0019</reply-code>'
                       '</get-record>'.encode()))
        yield m


def _fixtures(path):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(current_dir, 'fixtures', path)
