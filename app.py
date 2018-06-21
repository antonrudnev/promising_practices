from flask import Flask, redirect, render_template, request, url_for
import pysolr
from settings import SOLR, ITEMS_PER_PAGE, PAGER_RANGE, STATES

app = Flask(__name__)
solr = pysolr.Solr(SOLR)


@app.route("/")
def list_practices():
    page = int(request.args.get("page", 0))
    query = request.args.get("query", "").strip()
    query = query if query else "*:*"
    response = solr.search(query, **{"start": page * ITEMS_PER_PAGE,
                                     "rows": ITEMS_PER_PAGE,
                                     "sort": "id_int asc",
                                     "wt": "json"}).raw_response
    max_page = int(response["response"]["numFound"] / ITEMS_PER_PAGE)
    pages = []
    for p in range(page - PAGER_RANGE, page + PAGER_RANGE + 1):
        if 0 <= p <= max_page:
            pages.append(p)
    if pages[0] > 1:
        pages.insert(0, "...")
    if pages[0] != 0:
        pages.insert(0, 0)
    if pages[-1] < max_page - 1:
        pages.append("...")
    if pages[-1] != max_page:
        pages.append(max_page)
    return render_template("get_practices.html", practices=response["response"]["docs"],
                           page=page,
                           pages=pages,
                           query=query)


@app.route("/practice/<int:practice_id>")
@app.route("/practice/edit/<int:practice_id>")
def get_practice(practice_id):
    page = int(request.args.get("page"))
    query = request.args.get("query")
    response = solr.search("id:{}".format(practice_id), **{"rows": 1, "wt": "json"}).raw_response
    return render_template("edit_practice.html" if "edit" in request.path else "get_practice.html",
                           practice=response["response"]["docs"][0],
                           page=page,
                           query=query,
                           states=STATES if "edit" in request.path else None)


@app.route("/practice/<int:practice_id>", methods=["POST"])
def update_status_practice(practice_id):
    page = int(request.args.get("page"))
    query = request.args.get("query")
    if request.form["status"] in ["DRAFT", "REVOKED"]:
        new_status = "APPROVED"
    else:
        new_status = "REVOKED"
    solr.add([{"id": str(practice_id), "status": new_status}], fieldUpdates={"status": "set"}, commit=False, softCommit=True)
    return redirect(url_for("list_practices", page=page, query=query))


@app.route("/practice/edit/<int:practice_id>", methods=["POST"])
def update_practice(practice_id):
    page = int(request.args.get("page"))
    query = request.args.get("query")
    solr.add([request.form.to_dict(flat=False)], commit=False, softCommit=True)
    return redirect("/practice/{}?page={}&query={}".format(practice_id, page, query))


if __name__ == "__main__":
    app.run()
