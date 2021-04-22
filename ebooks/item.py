import boto3
from flask import Blueprint, current_app, render_template
import requests

from ebooks.auth import login_required
from ebooks.queries import get_filenames, get_metadata, get_url, get_volumes


bp = Blueprint('item', __name__, url_prefix='/item')


@bp.route("/<item>")
@login_required
def item(item="None"):
    s3 = boto3.client(
        's3',
        aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY'],
        region_name=current_app.config['AWS_REGION_NAME']
        )
    bucket = current_app.config['AWS_BUCKET_NAME']

    try:
        record = requests.get("https://library.mit.edu/rest-dlf/record/mit01" +
                              item + "?view=full&key=" +
                              current_app.config['ALEPH_API_KEY'])
        marc_xml = record.content
        metadata = get_metadata(marc_xml)
    except AttributeError:
        metadata = {'Error': 'Item not found.'}

    files = []
    try:
        filenames = get_filenames(s3, bucket, item)
        for f in filenames:
            files.append({'name': f, 'url': get_url(s3, bucket, f)})
    except KeyError:
        pass

    fields = ['Title', 'Author', 'Edition', 'Publication', 'Series', 'ISBN',
              'ISSN', 'Original Version', 'Error']

    if 'Serial' in metadata:
        volumes = get_volumes(files)
        return render_template("serial.html", file_id=item, files=files,
                               metadata=metadata, fields=fields,
                               volumes=volumes)
    else:
        return render_template("landing.html", file_id=item, files=files,
                               metadata=metadata, fields=fields)
