from ebooks import app
from flask import abort, render_template, send_file
from queries import get_file, get_filenames, get_metadata


@app.route("/")
@app.route("/<item>")
def index(item="002341336"):
    files = get_filenames(item)
    metadata = get_metadata(item)
    fields = ['Title', 'Author', 'Edition', 'Publication', 'Series', 'ISBN',
              'ISSN', 'Error']
    return render_template("landing.html", file_id=item, files=files,
                           metadata=metadata, fields=fields)


@app.route('/docs/<filename>')
def file(filename):
    if '..' in filename or filename.startswith('/'):
        abort(404)
    obj = get_file(filename)
    if obj == 404:
        abort(404)
    else:
        return send_file(obj['Body'], mimetype=obj['ContentType'])
