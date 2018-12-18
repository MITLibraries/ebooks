from ebooks.queries import get_file, get_filenames, get_metadata, get_volumes


def test_get_filenames(s3_conn):
    names = get_filenames('sample_01')
    assert 'sample_01-a.txt' in names
    assert 'sample_01-b.txt' in names


def test_get_file(s3_conn):
    f = get_file('sample_01-a.txt')
    assert f['ContentType'] == 'text/plain'


def test_get_nonexistent_file_returns_404(s3_conn):
    f = get_file('not_a_file.txt')
    assert f == 404


def test_get_metadata_from_record(record):
    r = get_metadata(record)
    assert r['Title'] == 'Title Subtitle'


def test_get_volumes():
    v = get_volumes(['has_volumes_a_2009.txt', 'has_volumes_b_2009.txt'])
    assert '2009' in v
