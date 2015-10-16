import requests
import settings
import xml.etree.ElementTree as ET
from boto3 import Session
import botocore


def get_filenames(file_id):
    RESULTS = []
    files = []
    session = Session(aws_access_key_id=settings.aws_access_key_id,
                      aws_secret_access_key=settings.aws_secret_access_key,
                      region_name=settings.region_name)
    s3 = session.resource('s3')
    bucket = s3.Bucket('mit-ebooks')

    for key in bucket.objects.all():
        files.append(key.key)

    for f in files:
        try:
            p = f.index('.')
            item_name = f[:p]
        except:
            pass

        try:
            i = f.index('_')
            item_name = f[:i]
        except:
            pass

        if item_name == file_id:
            RESULTS.append(f)

    RESULTS.sort()

    return RESULTS


def get_url(file_name):
    session = botocore.session.get_session()
    client = session.create_client('s3',
                                   aws_access_key_id=settings.
                                   aws_access_key_id,
                                   aws_secret_access_key=settings.
                                   aws_secret_access_key,
                                   region_name='us-east-1')

    url = client.generate_presigned_url('get_object',
                                        Params={'Bucket': 'mit-ebooks',
                                                'Key': file_name},
                                        ExpiresIn=86400)

    return url


def get_file(file_name):
    RESULTS = {}
    session = botocore.session.get_session()
    client = session.create_client('s3',
                                   aws_access_key_id=settings.
                                   aws_access_key_id,
                                   aws_secret_access_key=settings.
                                   aws_secret_access_key,
                                   region_name='us-east-1')
    try:
        obj = client.get_object(Bucket='mit-ebooks', Key=file_name)
        return obj
    except:
        return 404


def get_metadata(file_id):
    RESULTS = {}

    try:
        r = requests.get("http://walter.mit.edu/rest-dlf/record/mit01" +
                         file_id + "?view=full")
        metadata = r.content

        record = ET.fromstring(metadata).find('record')

        fields = record.findall("./datafield")
        for field in fields:

                isbn = get_field_value(field, '020', 'a')
                if isbn:
                    RESULTS['ISBN'] = isbn

                issn = get_field_value(field, '022', 'a')
                if issn:
                    RESULTS['ISSN'] = issn

                series = get_field_value(field, '830', 'a')
                series_num = get_field_value(field, '830', 'v')
                if series:
                    if series_num:
                        series += series_num
                    RESULTS['Series'] = series

                pub_info = get_field_value(field, '260', 'all')
                if not pub_info:
                    pub_info = get_field_value(field, '264', 'all')
                if pub_info:
                    RESULTS['Publication'] = pub_info

                edition = get_field_value(field, '250', 'a')
                if edition:
                    RESULTS['Edition'] = edition

                author = get_field_value(field, '100', 'a')
                if author:
                    author = author.rstrip('. ')
                    RESULTS['Author'] = author

                title = get_field_value(field, '245', 'a')
                subtitle = get_field_value(field, '245', 'b')
                if title:
                    title = title.rstrip('/ ')
                    if subtitle:
                        title += subtitle
                    RESULTS['Title'] = title

    except:
        RESULTS['Error'] = 'Item not found.'

    return RESULTS


def get_field_value(parent, marc_field, subcode):
    if parent.attrib.get('tag') == marc_field:
        fieldElements = parent.getchildren()
        field_value = ''
        for item in fieldElements:
            if subcode == 'all':
                field_value += item.text + ' '
            elif item.attrib.get('code') == subcode:
                field_value = item.text
                return field_value
        return field_value
    else:
        return False

if __name__ == "__main__":
    print get_file('002341336.pdf')
