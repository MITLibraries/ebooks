def test_item_page_redirects_if_not_authenticated(testapp):
    response = testapp.get('/item/sample-monograph')
    assert response.status_code == 302
    assert 'next=http%3A%2F%2Flocalhost%2Fitem%2Fsample-monograph' \
        in response.location


def test_item_page_loads_if_authenticated(testapp, client, s3_conn, aleph):
    response = client.get('/item/sample')
    assert response.status_code == 200


def test_item_page_displays_video_correctly(testapp, client, s3_conn, aleph):
    response = client.get('/item/sample')
    assert b'<video width="100%" height="auto" controls>' in response.data


def test_load_index_nonexistent_item(testapp, client, s3_conn, aleph):
    response = client.get('/item/fake_item')
    assert b'Item not found' in response.data


def test_load_serial_item(testapp, client, s3_conn, aleph):
    response = client.get('/item/serial')
    assert response.status_code == 200


def test_get_file_success(testapp, client, s3_conn):
    response = client.get('/docs/sample_01-a.txt')
    assert response.content_type == 'text/plain; charset=utf-8'


def test_get_bad_file(testapp, client, s3_conn):
    response = client.get('/docs/0023..41336.pdf')
    assert response.status_code == 404


def test_get_nonexistent_file(testapp, client, s3_conn):
    response = client.get('/docs/fake_file.pdf')
    assert response.status_code == 404
