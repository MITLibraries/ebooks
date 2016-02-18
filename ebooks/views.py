from ebooks import app
from flask import render_template
from queries import get_filenames, get_metadata, get_volumes
import requests


@app.route("/")
@app.route("/<item>")
def index(item="002341336"):
    files = get_filenames(item)

    metadata = {}
    try:
        record = requests.get("http://library.mit.edu/rest-dlf/record/mit01" +
                              item + "?view=full")
        marc_xml = record.content
        metadata = get_metadata(marc_xml)
    except:
        metadata['Error'] = 'Item not found.'

    fields = ['Title', 'Author', 'Edition', 'Publication', 'Series', 'ISBN',
              'ISSN', 'Error']

    if 'Serial' in metadata:
        volumes = get_volumes(files)
        return render_template("serial.html", file_id=item, files=files,
                               metadata=metadata, fields=fields,
                               volumes=volumes)
    else:
        return render_template("landing.html", file_id=item, files=files,
                               metadata=metadata, fields=fields)
