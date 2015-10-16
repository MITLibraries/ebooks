from flask import Flask
from flask import render_template, redirect, send_file, make_response, abort
from queries import get_filenames, get_metadata, get_url, get_file


app = Flask(__name__)


@app.route("/")
@app.route("/<item>")
def index(item="002341336"):
    files = get_filenames(item)
    metadata = get_metadata(item)

    return render_template("landing.html", file_id=item, files=files,
                           metadata=metadata)


@app.route('/s3/<path:path>')
def s3_file(path):
    url = get_url(path)
    return redirect(url, code=301)


@app.route('/obj/<filename>')
def file(filename):
    if '..' in filename or filename.startswith('/'):
        abort(404)
    obj = get_file(filename)
    if type(obj) == int:
        abort(404)
    else:
        return send_file(obj['Body'], mimetype=obj['ContentType'])


@app.route('/docs/<filename>')
def get_doc(filename):
    obj = get_file(filename)
    response = make_response(send_file(obj['Body']))
    response.headers['Content-Type'] = obj['ContentType']
    response.headers['Content-Disposition'] = 'inline; filename=' + filename

    print response.headers
    return response


if __name__ == "__main__":
    app.run(debug=True)
