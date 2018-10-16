from flask import Blueprint, jsonify
from settings import COUNTER_QUERIES, SOLR_COLLECTION
from pysolr import Solr

bp = Blueprint("api", __name__, url_prefix="/api/v1")
solr = Solr(SOLR_COLLECTION)


@bp.route("/counter", methods=["GET"])
def index():
    counters = dict()
    for counter_name in COUNTER_QUERIES.keys():
        response = solr.search("*:*", **{"rows": 0, "wt": "json", "fq": COUNTER_QUERIES[counter_name]})
        counters[counter_name] = response.hits
    return jsonify(counters)
