from auth import login_required, permission_required
from db import get_comments, get_master_dictionary, delete_comments, read_mention, insert_comment
from flask import Blueprint, flash, g, redirect, render_template, request, url_for
import functools
from math import ceil
from pysolr import Solr, SolrError
from settings import SOLR_COLLECTION, ITEMS_PER_PAGE, PAGER_RANGE, WORKFLOW, STATUS_BADGE_STYLE
from workspace import push_mentions

bp = Blueprint('practice', __name__, url_prefix="/practice/")
solr = Solr(SOLR_COLLECTION)


def get_next_state(current, action=None):
    return [i for i in WORKFLOW if i["current"] == current and (not action or i["action"] == action)]


def exists_check(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        id = kwargs["id"]
        response = solr.search("id:{}".format(id), **{"rows": 1, "wt": "json",
                                                      "mlt": "true", "mlt.fl": "summary",
                                                      "mlt.mintf": 1, "mlt.mindf": 1})
        docs = response.docs
        if len(docs) == 0:
            flash({"status": "alert-danger", "text": "Item {} doesn't exist.".format(id)})
            return redirect(url_for("practice.index"))
        g.document = docs[0]
        g.more_like_this = response.raw_response["moreLikeThis"][str(id)]["docs"]
        return view(**kwargs)

    return wrapped_view


@bp.route("/index/")
@login_required
@push_mentions
def index():
    get_master_dictionary()
    page = int(request.args.get("page", 0))
    query = request.args.get("query", "").strip()
    query = query if query else "*:*"
    view_permissions = [p[5:] for p in g.permissions if p.startswith("VIEW_")]
    fq = "status:({})".format(" OR ".join(view_permissions)) if view_permissions else "status:none"
    try:
        response = solr.search(query, **{"start": page * ITEMS_PER_PAGE, "rows": ITEMS_PER_PAGE,
                                         "sort": "_id_int asc", "wt": "json", "fq": fq})
    except SolrError:
        flash({"status": "alert-danger", "text": "Invalid query string. Check the Solr query syntax reference guide."})
        return redirect(url_for("practice.index", page=0, query="*:*"))

    max_page = max(int(ceil(response.hits / ITEMS_PER_PAGE) - 1), 0)
    if request.args.get("go_to_last_page", False):
        page = max_page
        response = solr.search(query, **{"start": page * ITEMS_PER_PAGE, "rows": ITEMS_PER_PAGE,
                                         "sort": "_id_int asc", "wt": "json", "fq": fq})
    pager = [p for p in range(page - PAGER_RANGE, page + PAGER_RANGE + 1) if 0 <= p <= max_page]
    if pager[0] > 1:
        pager.insert(0, "...")
    if pager[0] != 0:
        pager.insert(0, 0)
    if pager[-1] < max_page - 1:
        pager.append("...")
    if pager[-1] != max_page:
        pager.append(max_page)
    return render_template("practice/index.html", practices=response.docs, page=page, pager=pager, query=query)


@bp.route("/create/", methods=["GET", "POST"])
@login_required
@permission_required("ACTION_CREATE")
def create():
    page = int(request.args.get("page", 0))
    query = request.args.get("query", "").strip()
    query = query if query else "*:*"

    if request.method == "POST":
        docs = solr.search("*:*", **{"sort": "_id_int desc", "rows": 1,
                                     "fl": "_id_int", "wt": "json"}).docs
        max_id = docs[0]["_id_int"] if len(docs) > 0 else 0
        doc = request.form.to_dict(flat=False)
        doc["id"] = max_id + 1
        solr.add([doc], commit=False, softCommit=True)
        flash({"status": "alert-success", "text": "New item has been successfully created."})
        insert_comment(doc["id"], g.user["id"], "Document has been <mark>created</mark>.")
        return redirect(url_for("practice.index", go_to_last_page=True))

    return render_template("practice/create.html", page=page, query=query, master=get_master_dictionary())


@bp.route("/<int:id>/", methods=["GET"])
@login_required
@exists_check
@permission_required("VIEW", rule="status_based")
def details(id):
    page = int(request.args.get("page", 0))
    query = request.args.get("query", "").strip()
    query = query if query else "*:*"
    comments = get_comments(id)
    read_mention(g.user["id"], id)
    view_permissions = [p[5:] for p in g.permissions if p.startswith("VIEW_")]
    # g.document["summary"] = repr(g.document["summary"])[1:-1]
    return render_template("practice/details.html", practice=g.document, comments=comments, page=page, query=query,
                           master=get_master_dictionary(), actions=get_next_state(g.document["status"]),
                           more_like_this=g.more_like_this, view_permissions=view_permissions)


@bp.route("/<int:id>/action/", methods=["POST"])
@login_required
@exists_check
@permission_required("ACTION", rule="action_based")
def action(id):
    page = int(request.args.get("page", 0))
    query = request.args.get("query", "").strip()
    query = query if query else "*:*"
    next_states = get_next_state(g.document["status"], request.form["action"].upper())

    if len(next_states) != 0:
        next_status = next_states[0]["next"]
        solr.add([{"id": str(id), "status": next_status}], fieldUpdates={"status": "set"}, commit=False,
                 softCommit=True)
        flash({"status": "alert-{}".format(STATUS_BADGE_STYLE[next_status]),
               "text": "Item {} has been successfully {}.".format(id, next_status)})
        insert_comment(id, g.user["id"], "Document has been <mark>{}</mark>.".format(next_status.lower()))
    else:
        flash({"status": "alert-danger", "text": "Item {} status update failure due to version conflict.".format(id)})
        return redirect(url_for("practice.details", id=id, page=page, query=query))

    return redirect(url_for("practice.index", page=page, query=query))


@bp.route("/<int:id>/comment/", methods=["POST"])
@login_required
@exists_check
def comment(id):
    page = int(request.args.get("page", 0))
    query = request.args.get("query", "").strip()
    query = query if query else "*:*"
    insert_comment(id, g.user["id"], request.form["comment"])
    return redirect(url_for("practice.details", id=id, page=page, query=query))


@bp.route("/<int:id>/edit/", methods=["GET", "POST"])
@login_required
@exists_check
@permission_required("EDIT", rule="status_based")
def edit(id):
    page = int(request.args.get("page", 0))
    query = request.args.get("query", "").strip()
    query = query if query else "*:*"

    if request.method == "POST":
        try:
            solr.add([request.form.to_dict(flat=False)], commit=False, softCommit=True)
            flash({"status": "alert-success", "text": "Item {} has been successfully updated.".format(id)})
        except SolrError:
            flash({"status": "alert-danger", "text": "Item {} update failure due to version conflict.".format(id)})
        return redirect(url_for("practice.details", id=id, page=page, query=query))

    return render_template("practice/edit.html", practice=g.document, page=page, query=query,
                           master=get_master_dictionary())


@bp.route("/<int:id>/delete/", methods=["GET", "POST"])
@login_required
@exists_check
@permission_required("DELETE", rule="status_based")
def delete(id):
    page = int(request.args.get("page", 0))
    query = request.args.get("query", "").strip()
    query = query if query else "*:*"

    if request.method == "POST":
        solr.delete(id, commit=False, softCommit=True)
        flash({"status": "alert-success", "text": "Item {} has been successfully deleted.".format(id)})
        delete_comments(id)
        return redirect(url_for("practice.index", page=page, query=query))

    title = request.args.get("title")
    return render_template("practice/delete.html", id=id, title=title, page=page, query=query)
