from auth import login_required, permission_required
from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from math import ceil
import pysolr
from settings import SOLR, ITEMS_PER_PAGE, PAGER_RANGE, WORKFLOW, ACTION_STYLE, STATUS_BADGE_STYLE, STATUS_STYLE_INDEX
from settings import IMPLEMENTERS, INTERVENTION_GOALS, POPULATIONS, PROGRAM_COMPONENTS, STATES

bp = Blueprint('practice', __name__, url_prefix="/practice")
solr = pysolr.Solr(SOLR)


def get_next_state(current, action=None):
    return [i for i in WORKFLOW if i["current"] == current and (not action or i["action"] == action)]


@bp.route("/")
@login_required
def index():
    try:
        page = int(request.args.get("page", 0))
        query = request.args.get("query", "").strip()
        query = query if query else "*:*"
        view_permissions = [p[5:] for p in g.permissions if p.startswith("VIEW_")]
        fq = "status:({})".format(" OR ".join(view_permissions)) if view_permissions else "status:none"
        response = solr.search(query, **{"start": page * ITEMS_PER_PAGE, "rows": ITEMS_PER_PAGE,
                                         "sort": "id_int asc", "wt": "json", "fq": fq}).raw_response
        max_page = max(int(ceil(response["response"]["numFound"] / ITEMS_PER_PAGE) - 1), 0)
        if request.args.get("go_to_last_page", False):
            page = max_page
            response = solr.search(query, **{"start": page * ITEMS_PER_PAGE, "rows": ITEMS_PER_PAGE,
                                             "sort": "id_int asc", "wt": "json", "fq": fq}).raw_response
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
                               page=page, pager=pager, query=query, styles=STATUS_STYLE_INDEX)
    except Exception as e:
        flash({"status": "alert-danger", "text": "Invalid query string. Check Solr query syntax reference."})
        return redirect(url_for("practice.index", page=0, query="*:*"))


@bp.route("/create", methods=["GET", "POST"])
@login_required
@permission_required("ACTION_CREATE")
def create():
    page = int(request.args.get("page", 0))
    query = request.args.get("query", "").strip()
    query = query if query else "*:*"

    if request.method == "POST":
        max_id = solr.search("*:*", **{"sort": "id_int desc", "rows": 1,
                                       "fl": "id_int", "wt": "json"}).raw_response["response"]["docs"][0]["id_int"]
        doc = request.form.to_dict(flat=False)
        doc["id"] = max_id + 1
        solr.add([doc], commit=False, softCommit=True)
        flash({"status": "alert-success", "text": "New item has been successfully created."})
        return redirect(url_for("practice.index", go_to_last_page=True))

    return render_template("practice/create.html", page=page, query=query,
                           states=STATES, intervention_goals=INTERVENTION_GOALS, implementers=IMPLEMENTERS,
                           program_components=PROGRAM_COMPONENTS, populations=POPULATIONS)


@bp.route("/<int:id>", methods=["GET"])
@login_required
@permission_required("VIEW", rule="status_based")
def details(id):
    page = int(request.args.get("page", 0))
    query = request.args.get("query", "").strip()
    query = query if query else "*:*"
    doc = solr.search("id:{}".format(id), **{"rows": 1, "wt": "json"}).raw_response["response"]["docs"][0]
    return render_template("practice/details.html", practice=doc, page=page, query=query,
                           states=STATES, intervention_goals=INTERVENTION_GOALS, implementers=IMPLEMENTERS,
                           program_components=PROGRAM_COMPONENTS, populations=POPULATIONS,
                           actions=get_next_state(doc["status"]), styles={**ACTION_STYLE, **STATUS_BADGE_STYLE})


@bp.route("/<int:id>", methods=["POST"])
@login_required
@permission_required("ACTION", rule="action_based")
def action(id):
    page = int(request.args.get("page", 0))
    query = request.args.get("query", "").strip()
    query = query if query else "*:*"
    doc = solr.search("id:{}".format(id), **{"rows": 1, "wt": "json"}).raw_response["response"]["docs"][0]
    next_status = get_next_state(doc["status"], request.form["action"].upper())[0]["next"]
    solr.add([{"id": str(id), "status": next_status}], fieldUpdates={"status": "set"}, commit=False, softCommit=True)
    flash({"status": "alert-{}".format(STATUS_BADGE_STYLE[next_status]),
           "text": "Item {} has been successfully {}.".format(id, next_status)})
    return redirect(url_for("practice.index", page=page, query=query))


@bp.route("/<int:id>/edit", methods=["GET", "POST"])
@login_required
@permission_required("EDIT", rule="status_based")
def edit(id):
    page = int(request.args.get("page", 0))
    query = request.args.get("query", "").strip()
    query = query if query else "*:*"

    if request.method == "POST":
        solr.add([request.form.to_dict(flat=False)], commit=False, softCommit=True)
        flash({"status": "alert-success", "text": "Item {} has been successfully updated.".format(id)})
        return redirect(url_for("practice.details", id=id, page=page, query=query))

    doc = solr.search("id:{}".format(id), **{"rows": 1, "wt": "json"}).raw_response["response"]["docs"][0]
    return render_template("practice/edit.html", practice=doc, page=page, query=query,
                           states=STATES, intervention_goals=INTERVENTION_GOALS, implementers=IMPLEMENTERS,
                           program_components=PROGRAM_COMPONENTS, populations=POPULATIONS, styles=STATUS_BADGE_STYLE)


@bp.route("/<int:id>/delete", methods=["GET", "POST"])
@login_required
@permission_required("DELETE", rule="status_based")
def delete(id):
    page = int(request.args.get("page", 0))
    query = request.args.get("query", "").strip()
    query = query if query else "*:*"

    if request.method == "POST":
        solr.delete(id, commit=False, softCommit=True)
        flash({"status": "alert-success", "text": "Item {} has been successfully deleted.".format(id)})
        return redirect(url_for("practice.index", page=page, query=query))

    title = request.args.get("title")
    return render_template("practice/delete.html", id=id, title=title, page=page, query=query)
