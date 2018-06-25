from flask import Blueprint, redirect, render_template, request, url_for
from math import ceil
import pysolr
from settings import SOLR, ITEMS_PER_PAGE, PAGER_RANGE
from settings import STATES, INTERVENTION_GOALS, IMPLEMENTERS, PROGRAM_COMPONENTS, POPULATIONS

bp = Blueprint('practice', __name__, url_prefix="/practice")
solr = pysolr.Solr(SOLR)


@bp.route("/")
def index():
    page = int(request.args.get("page", 0))
    query = request.args.get("query", "").strip()
    query = query if query else "*:*"
    response = solr.search(query, **{"start": page * ITEMS_PER_PAGE, "rows": ITEMS_PER_PAGE,
                                     "sort": "id_int asc", "wt": "json"}).raw_response
    max_page = max(int(ceil(response["response"]["numFound"] / ITEMS_PER_PAGE) - 1), 0)
    if request.args.get("go_to_last_page", False):
        page = max_page
        response = solr.search(query, **{"start": page * ITEMS_PER_PAGE, "rows": ITEMS_PER_PAGE,
                                         "sort": "id_int asc", "wt": "json"}).raw_response
    pager = [p for p in range(page - PAGER_RANGE, page + PAGER_RANGE + 1) if 0 <= p <= max_page]
    if pager[0] > 1:
        pager.insert(0, "...")
    if pager[0] != 0:
        pager.insert(0, 0)
    if pager[-1] < max_page - 1:
        pager.append("...")
    if pager[-1] != max_page:
        pager.append(max_page)
    return render_template("practice/index.html", practices=response["response"]["docs"],
                           page=page, pager=pager, query=query)


@bp.route("/create", methods=["GET", "POST"])
def create():
    page = int(request.args.get("page"))
    query = request.args.get("query")

    if request.method == "POST":
        max_id = solr.search("*:*", **{"sort": "id_int desc", "rows": 1,
                                       "fl": "id_int", "wt": "json"}).raw_response["response"]["docs"][0]["id_int"]
        doc = request.form.to_dict(flat=False)
        doc["id"] = max_id + 1
        solr.add([doc], commit=False, softCommit=True)
        return redirect(url_for("practice.index", go_to_last_page=True))

    return render_template("practice/create.html", page=page, query=query, states=STATES,
                           intervention_goals=INTERVENTION_GOALS, implementers=IMPLEMENTERS,
                           program_components=PROGRAM_COMPONENTS, populations=POPULATIONS)


@bp.route("/<int:id>", methods=["GET", "POST"])
def details(id):
    page = int(request.args.get("page"))
    query = request.args.get("query")
    if request.method == "POST":
        if request.form["status"] in ["DRAFT", "REVOKED"]:
            new_status = "APPROVED"
        else:
            new_status = "REVOKED"
        solr.add([{"id": str(id), "status": new_status}], fieldUpdates={"status": "set"}, commit=False,
                 softCommit=True)
        return redirect(url_for("practice.index", page=page, query=query))

    doc = solr.search("id:{}".format(id), **{"rows": 1, "wt": "json"}).raw_response["response"]["docs"][0]
    return render_template("practice/details.html", practice=doc, page=page, query=query, states=STATES,
                           intervention_goals=INTERVENTION_GOALS, implementers=IMPLEMENTERS,
                           program_components=PROGRAM_COMPONENTS, populations=POPULATIONS)


@bp.route("/<int:id>/edit", methods=["GET", "POST"])
def edit(id):
    page = int(request.args.get("page"))
    query = request.args.get("query")
    if request.method == "POST":
        solr.add([request.form.to_dict(flat=False)], commit=False, softCommit=True)
        return redirect(url_for("practice.details", id=id, page=page, query=query))

    doc = solr.search("id:{}".format(id), **{"rows": 1, "wt": "json"}).raw_response["response"]["docs"][0]
    return render_template("practice/edit.html", practice=doc, page=page, query=query, states=STATES,
                           intervention_goals=INTERVENTION_GOALS, implementers=IMPLEMENTERS,
                           program_components=PROGRAM_COMPONENTS, populations=POPULATIONS)


@bp.route("/<int:id>/delete", methods=["GET", "POST"])
def delete(id):
    page = int(request.args.get("page"))
    query = request.args.get("query")
    if request.method == "POST":
        solr.delete(id, commit=False, softCommit=True)
        return redirect(url_for("practice.index", page=page, query=query))
    title = request.args.get("title")
    return render_template("practice/delete.html", id=id, title=title, page=page, query=query)
