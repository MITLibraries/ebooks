def test_item_page_redirects_if_not_authenticated(app):
    with app.test_client() as client:
        response = client.get('/item/sample-monograph')
        assert response.status_code == 302
        assert 'next=http%3A%2F%2Flocalhost%2Fitem%2Fsample-monograph' \
            in response.location


def test_item_page_loads_if_authenticated(app, client, s3_conn, aleph):
    response = client.get('/item/sample')
    assert response.status_code == 200


def test_item_page_displays_video_correctly(app, client, s3_conn, aleph):
    response = client.get('/item/sample')
    assert b'<video width="100%" height="auto" controls>' in response.data


def test_load_index_nonexistent_item(app, client, s3_conn, aleph):
    response = client.get('/item/fake_item')
    assert b'Item not found' in response.data


def test_load_serial_item(app, client, s3_conn, aleph):
    response = client.get('/item/serial')
    assert response.status_code == 200
