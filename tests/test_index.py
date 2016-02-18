from __future__ import absolute_import

from ebooks.queries import get_metadata


def test_index_page_loads(testapp):
    response = testapp.get('/')
    assert response.status_code == 200


def test_load_index_nonexistent_item(testapp):
    response = testapp.get('/12345')
    assert 'Item not found' in response


def test_load_serial_item(testapp):
    response = testapp.get('/002341337')
    assert response.status_code == 200


def test_get_file_success(testapp):
    response = testapp.get('/static/files/002341336.pdf')
    assert response.content_type == 'application/pdf'


def test_get_nonexistent_file(testapp):
    response = testapp.get('/static/files/fake_file.pdf', status=404)
    assert response.status_code == 404


def test_get_metadata_from_record(app, record):
    r = get_metadata(record)
    assert r['Title'] == 'Title Subtitle'
