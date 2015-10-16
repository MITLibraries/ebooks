from flask import Flask
from flask import abort, render_template, send_file
from queries import get_file, get_filenames, get_metadata


app = Flask(__name__)


@app.route("/")
@app.route("/<item>")
def index(item="002341336"):
    files = get_filenames(item)
    metadata = get_metadata(item)
    return render_template("landing.html", file_id=item, files=files,
                           metadata=metadata)


@app.route('/docs/<filename>')
def file(filename):
    if '..' in filename or filename.startswith('/'):
        abort(404)
    obj = get_file(filename)
    if obj == 404:
        abort(404)
    else:
        return send_file(obj['Body'], mimetype=obj['ContentType'])


if __name__ == "__main__":
    app.run(debug=True)
