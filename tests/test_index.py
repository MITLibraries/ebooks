from __future__ import absolute_import


def test_index_page_loads(testapp):
    response = testapp.get('/')
    assert response.status_code == 200
