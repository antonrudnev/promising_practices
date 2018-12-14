from flask import abort, Blueprint, jsonify, request
from db import insert_demo_request
from settings import COUNTER_QUERIES, SOLR_COLLECTION
from pysolr import Solr

import json

bp = Blueprint("api", __name__, url_prefix="/api/v1")
solr = Solr(SOLR_COLLECTION)


@bp.route("/counter", methods=["GET"])
def counter():
    counters = dict()
    for counter_name in COUNTER_QUERIES.keys():
        response = solr.search("*:*", **{"rows": 0, "wt": "json", "fq": COUNTER_QUERIES[counter_name]})
        counters[counter_name] = response.hits
    return jsonify(counters)


@bp.route("/demorequest", methods=["POST"])
def demo_request():
    try:
        required_fields = ["first_name", "last_name", "organization_name", "email"]
        request_details = request.json
        if any(x not in request_details for x in required_fields):
            return abort(400)
        insert_demo_request(json.dumps(request_details))
        return jsonify("Request received"), 201
    except Exception:
        return abort(500)
