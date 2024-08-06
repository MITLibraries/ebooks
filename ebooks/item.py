import boto3
from botocore.client import Config
from flask import Blueprint, current_app, render_template
import requests

from ebooks.auth import login_required
from ebooks.queries import get_filenames, get_metadata, get_url, get_volumes


bp = Blueprint("item", __name__, url_prefix="/item")


@bp.route("/<item>")
@login_required
def item(item="None"):
    s3 = boto3.client(
        "s3",
        region_name=current_app.config["AWS_REGION_NAME"],
        config=Config(signature_version="s3v4"),
    )
    bucket = current_app.config["AWS_BUCKET_NAME"]

    try:
        base_alma_url = current_app.config["ALMA_API_URL"]
        url = base_alma_url + item + "?apikey=" + current_app.config["ALMA_API_KEY"]
        record = requests.get(url)
        marc_xml = record.content
        metadata = get_metadata(marc_xml)
    except AttributeError:
        metadata = {"Error": "Item not found."}

    files = []
    try:
        filenames = get_filenames(s3, bucket, item)
        for f in filenames:
            files.append({"name": f, "url": get_url(s3, bucket, f)})
    except KeyError:
        pass

    fields = [
        "Title",
        "Author",
        "Edition",
        "Publication",
        "Series",
        "ISBN",
        "ISSN",
        "Original Version",
        "Error",
    ]

    if "Serial" in metadata:
        volumes = get_volumes(files)
        return render_template(
            "serial.html",
            file_id=item,
            files=files,
            metadata=metadata,
            fields=fields,
            volumes=volumes,
        )
    else:
        return render_template(
            "landing.html", file_id=item, files=files, metadata=metadata, fields=fields
        )

@bp.route("/debug")
def debug(): 
    return render_template("base.html")
