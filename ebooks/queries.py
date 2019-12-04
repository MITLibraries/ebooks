import os
import xml.etree.ElementTree as ET

import boto3

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION_NAME = os.getenv('AWS_REGION_NAME')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

s3 = boto3.client('s3',
                  aws_access_key_id=AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                  region_name=AWS_REGION_NAME)


def get_filenames(file_id):
    objs = s3.list_objects_v2(Bucket=AWS_BUCKET_NAME, Prefix=file_id)
    filenames = [o['Key'] for o in objs['Contents']]
    filenames.sort()
    return filenames


def get_url(s3_key):
    url = s3.generate_presigned_url(ClientMethod='get_object',
                                    Params={'Bucket': AWS_BUCKET_NAME,
                                            'Key': s3_key})
    return url


def get_metadata(metadata):
    RESULTS = {}

    record = ET.fromstring(metadata).find('record')
    leader = record.find('./leader').text
    if leader[7] == 's':
        RESULTS['Serial'] = True

    fields = record.findall("./datafield")
    for field in fields:
            title = get_field_value(field, '245', 'a')
            subtitle = get_field_value(field, '245', 'b')
            if title:
                title = title.rstrip('/ ')
                if subtitle:
                    title += ' ' + subtitle
                    title = title.rstrip('/ ')
                RESULTS['Title'] = title

            author = get_field_value(field, '100', 'a')
            if author:
                author = author.rstrip(',')
                RESULTS['Author'] = author

            edition = get_field_value(field, '250', 'a')
            if edition:
                RESULTS['Edition'] = edition

            pub_info = get_field_value(field, '260', 'all')
            if not pub_info:
                pub_info = get_field_value(field, '264', 'all')
            if pub_info:
                RESULTS['Publication'] = pub_info

            series = get_field_value(field, '830', 'a')
            series_num = get_field_value(field, '830', 'v')
            if series:
                if series_num:
                    series += series_num
                RESULTS['Series'] = series

            isbn = get_field_value(field, '020', 'a')
            if isbn:
                RESULTS['ISBN'] = isbn

            issn = get_field_value(field, '022', 'a')
            if issn:
                RESULTS['ISSN'] = issn

            original_version = get_field_value(field, '534', 'all')
            if original_version:
                RESULTS['Original Version'] = original_version

    return RESULTS


def get_field_value(parent, marc_field, subcode):
    if parent.attrib.get('tag') == marc_field:
        fieldElements = list(parent)
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


def get_volumes(files):
    volumes = {}
    for f in files:
        vol = f['name'].split('.', 1)[0][-4:]
        if vol not in volumes:
            volumes[vol] = [{'name': f['name'], 'url': f['url']}]
        else:
            volumes[vol].append({'name': f['name'], 'url': f['url']})
    print(volumes)
    return volumes
