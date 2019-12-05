from ebooks.queries import get_filenames, get_metadata, get_volumes


def test_get_filenames(s3_conn):
    names = get_filenames('sample_01')
    assert 'sample_01-a.txt' in names
    assert 'sample_01-b.txt' in names


def test_get_metadata_from_record(record):
    r = get_metadata(record)
    assert r['Title'] == 'Title Subtitle'


def test_get_volumes():
    v = get_volumes([{'name': 'has_volumes_a_2009.txt', 'url': 'fake'},
                     {'name': 'has_volumes_b_2009.txt', 'url': 'fake'}])
    assert '2009' in v
