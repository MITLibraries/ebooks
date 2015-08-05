from flask import Flask
from flask import render_template
from queries import get_filetypes, get_metadata

app = Flask(__name__)


@app.route("/")
@app.route("/<item>")
def index(item="001387502"):
	file_types = get_filetypes(item)
	metadata = get_metadata(item)
	return render_template("landing.html", file_id=item, file_types=file_types, metadata=metadata)

if __name__ == "__main__":
    app.run(debug=True)
