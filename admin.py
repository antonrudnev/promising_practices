from auth import login_required, permission_required
from db import get_master_data, get_roles, get_users, update_master_data, update_users_roles, update_roles_permissions
from flask import Blueprint, flash, redirect, render_template, request, Response, url_for
from os import path, mkdir
from pysolr import Solr
from settings import ALL_FIELDS, MULTIVALUED_FIELDS, SOLR_COLLECTION
from werkzeug.utils import secure_filename

import datetime
import json
import pandas as pd
import re

bp = Blueprint("admin", __name__, url_prefix="/admin")
solr = Solr(SOLR_COLLECTION)


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
    timestamp = re.sub(r"\D", "", str(datetime.datetime.now().replace(microsecond=0)))
    file_name = "opioid_interventions_{}.csv".format(timestamp)
    hits = solr.search("*:*", **{"rows": "0"}).hits
    documents = solr.search("*:*", **{"rows": hits}).docs
    for document in documents:
        for key in document.keys():
            if key in MULTIVALUED_FIELDS:
                document[key] = ",".join(document[key])
            # else:
            #     document[key] = repr(document[key])[1:-1]

    docs_json = json.dumps(documents)
    df = pd.read_json(docs_json, orient="records", dtype="category", encoding="utf-8").sort_values(by=["_id_int"])
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
    df = pd.read_csv(file_name, dtype="category", encoding="utf-8")
    documents = json.loads(df.to_json(orient="records"))
    for document in documents:
        for key in document.keys():
            if key in MULTIVALUED_FIELDS:
                value = document[key]
                if value:
                    document[key] = [x.strip() for x in value.split(",")]
    solr.add(documents)
    flash({"status": "alert-success", "text": "File has been successfully uploaded."})

    return redirect(url_for("practice.index"))


@bp.route("/master", methods=["GET", "POST"])
@login_required
@permission_required("ADMIN_MASTERDATA")
def master():
    if request.method == "POST":
        ids = request.form.getlist("id")
        categories = request.form.getlist("category")
        values = request.form.getlist("value")
        orders = request.form.getlist("order_number")
        deleted_ids = request.form.getlist("is_deleted")
        master_data = ({"category": category.strip(), "value": value.strip(), "order_number": order_number}
                       for id, category, value, order_number in zip(ids, categories, values, orders)
                       if id not in deleted_ids)
        update_master_data(master_data)
        flash({"status": "alert-success", "text": "Master data values have been successfully updated."})
    master_data = get_master_data()
    return render_template("admin/master.html", master=master_data)
