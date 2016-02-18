import os
import xml.etree.ElementTree as ET


def get_filenames(file_id):
    RESULTS = []
    files = []

    base_path = os.path.dirname(os.path.abspath(__file__))
    files_path = os.path.join(base_path, 'static/files')
    files = os.listdir(files_path)

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


def get_volumes(file_names):
    volumes = {}
    for f in file_names:
        vol = f.split('.', 1)[0][-4:]
        if vol not in volumes:
            volumes[vol] = [f]
        else:
            volumes[vol].append(f)
    return volumes
