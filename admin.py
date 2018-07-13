from auth import login_required, permission_required
import datetime
from db import get_roles, get_users, update_users_roles, update_roles_permissions
from flask import Blueprint, flash, redirect, render_template, request, Response, url_for
import json
from os import path, mkdir
import pandas as pd
from settings import ALL_FIELDS, MULTIVALUED_FIELDS, SOLR
from pysolr import Solr
from werkzeug.utils import secure_filename

bp = Blueprint("admin", __name__, url_prefix="/admin")
solr = Solr(SOLR)


@bp.route("/users", methods=["GET", "POST"])
@login_required
@permission_required("ADMIN_SECURITY")
def users():
    if request.method == "POST":
        assigned = request.form.getlist("assigned")
        enabled = request.form.getlist("enabled")
        update_users_roles(assigned, enabled)
        flash({"status": "alert-success", "text": "Security changes have been successfully applied."})
    users = get_users()
    return render_template("admin/users.html", users=users)


@bp.route("/roles", methods=["GET", "POST"])
@login_required
@permission_required("ADMIN_SECURITY")
def roles():
    if request.method == "POST":
        assigned = request.form.getlist("assigned")
        update_roles_permissions(assigned)
        flash({"status": "alert-success", "text": "Security changes have been successfully applied."})
    roles = get_roles()
    return render_template("admin/roles.html", roles=roles)


@bp.route("/download", methods=["GET"])
@login_required
@permission_required("ADMIN_CONTENT")
def download():
    file_name = "opioid_interventions {}.csv".format(datetime.datetime.now().replace(microsecond=0))
    hits = solr.search("*:*", **{"rows": "0"}).hits
    documents = solr.search("*:*", **{"rows": hits}).docs
    for document in documents:
        for key in document.keys():
            if key in MULTIVALUED_FIELDS:
                document[key] = ",".join(document[key])

    docs_json = json.dumps(documents)
    df = pd.read_json(docs_json, orient='records').sort_values(by=["id_int"])
    df.drop(columns=[c for c in df.columns.values if c not in ALL_FIELDS], inplace=True)

    return Response(
        df.reindex(columns=ALL_FIELDS).to_csv(index=False),
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename={}".format(file_name)})


@bp.route("/upload", methods=["POST"])
@login_required
@permission_required("ADMIN_CONTENT")
def upload():
    file = request.files["file"]
    if not path.exists("files"):
        mkdir("files")
    file_name = path.join("files", secure_filename(file.filename))
    file.save(file_name)
    df = pd.read_csv(file_name)
    documents = json.loads(df.to_json(orient="records"))
    for document in documents:
        for key in document.keys():
            if key in MULTIVALUED_FIELDS:
                value = document[key]
                if value:
                    document[key] = value.split(",")
    solr.add(documents)

    return redirect(url_for("practice.index"))
