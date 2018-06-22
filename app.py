from flask import Flask, redirect, render_template, request, url_for
import pysolr
from settings import SOLR, ITEMS_PER_PAGE, PAGER_RANGE
from settings import STATES, INTERVENTION_GOALS, IMPLEMENTERS, PROGRAM_COMPONENTS, POPULATIONS

app = Flask(__name__)
solr = pysolr.Solr(SOLR)


@app.route("/")
def list_practices():
    page = int(request.args.get("page", 0))
    query = request.args.get("query", "").strip()
    query = query if query else "*:*"
    response = solr.search(query, **{"start": page * ITEMS_PER_PAGE, "rows": ITEMS_PER_PAGE,
                                     "sort": "id_int asc", "wt": "json"}).raw_response
    max_page = int(response["response"]["numFound"] / ITEMS_PER_PAGE)
    pager = [p for p in range(page - PAGER_RANGE, page + PAGER_RANGE + 1) if 0 <= p <= max_page]
    if pager[0] > 1:
        pager.insert(0, "...")
    if pager[0] != 0:
        pager.insert(0, 0)
    if pager[-1] < max_page - 1:
        pager.append("...")
    if pager[-1] != max_page:
        pager.append(max_page)
    return render_template("list_practices.html", practices=response["response"]["docs"],
                           page=page, pager=pager, query=query)


@app.route("/practice/<int:practice_id>", methods=["GET", "POST"])
def get_practice(practice_id):
    page = int(request.args.get("page"))
    query = request.args.get("query")
    if request.method == "GET":
        doc = solr.search("id:{}".format(practice_id), **{"rows": 1, "wt": "json"}).raw_response["response"]["docs"][0]
        return render_template("get_practice.html", practice=doc, page=page, query=query)
    elif request.method == "POST":
        if request.form["status"] in ["DRAFT", "REVOKED"]:
            new_status = "APPROVED"
        else:
            new_status = "REVOKED"
        solr.add([{"id": str(practice_id), "status": new_status}], fieldUpdates={"status": "set"}, commit=False,
                 softCommit=True)
        return redirect(url_for("list_practices", page=page, query=query))
    else:
        pass


@app.route("/practice/edit/<int:practice_id>", methods=["GET", "POST"])
def edit_practice(practice_id):
    page = int(request.args.get("page"))
    query = request.args.get("query")
    if request.method == "GET":
        doc = solr.search("id:{}".format(practice_id), **{"rows": 1, "wt": "json"}).raw_response["response"]["docs"][0]
        return render_template("edit_practice.html", practice=doc, page=page, query=query, states=STATES,
                               intervention_goals=INTERVENTION_GOALS, implementers=IMPLEMENTERS,
                               program_components=PROGRAM_COMPONENTS, populations=POPULATIONS)
    elif request.method == "POST":
        solr.add([request.form.to_dict(flat=False)], commit=False, softCommit=True)
        return redirect(url_for("get_practice", practice_id=practice_id, page=page, query=query))
    else:
        pass


@app.route("/practice/create/", methods=["GET", "POST"])
def create_practice():
    page = int(request.args.get("page"))
    query = request.args.get("query")
    last = request.args.get("last")
    if request.method == "GET":
        return render_template("create_practice.html", page=page, query=query, last=last, states=STATES,
                               intervention_goals=INTERVENTION_GOALS, implementers=IMPLEMENTERS,
                               program_components=PROGRAM_COMPONENTS, populations=POPULATIONS)
    elif request.method == "POST":
        max_id = solr.search("*:*", **{"sort": "id_int desc", "rows": 1,
                                       "fl": "id_int", "wt": "json"}).raw_response["response"]["docs"][0]["id_int"]
        print(max_id)
        doc = request.form.to_dict(flat=False)
        doc["id"] = max_id + 1
        solr.add([doc], commit=False, softCommit=True)
        return redirect(url_for("list_practices", page=last, query=query))
    else:
        pass


if __name__ == "__main__":
    app.run()
