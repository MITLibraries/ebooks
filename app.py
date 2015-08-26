from flask import Flask
from flask import render_template
from queries import get_filenames, get_metadata

app = Flask(__name__)


@app.route("/")
@app.route("/<item>")
def index(item="002341336"):
	files = get_filenames(item)
	metadata = get_metadata(item)

	return render_template("landing.html", file_id=item, files=files, metadata=metadata)

if __name__ == "__main__":
    app.run(debug=True)
