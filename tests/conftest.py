import os

import boto3
import pytest
import requests_mock
from moto import mock_s3
from webtest import TestApp


@pytest.yield_fixture
def app():
    import ebooks
    app = ebooks.app
    app.config['ENV'] = 'testing'
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


@pytest.fixture(scope='function')
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'


@pytest.fixture(scope='function')
def s3_conn(aws_credentials):
    with mock_s3():
        conn = boto3.client('s3', region_name='us-east-1')
        conn.create_bucket(Bucket='samples')
        conn.put_object(Bucket='samples',
                        Key='sample_01-a.txt',
                        Body='I am a file. I live in a bucket.',
                        ContentType='text/plain')
        conn.put_object(Bucket='samples',
                        Key='sample_01-b.txt',
                        Body='I am a second file. I also live in the bucket.')
        conn.put_object(Bucket='samples',
                        Key='has_volumes_a_2009.txt',
                        Body='Vol 2009a')
        conn.put_object(Bucket='samples',
                        Key='has_volumes_b_2009.txt',
                        Body='Vol 2009b')
        conn.put_object(Bucket='samples',
                        Key='sample.mp4',
                        Body='fixtures/sample.mp4')
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
