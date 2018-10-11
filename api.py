from flask import Blueprint, jsonify
from settings import COUNTER_QUERIES, SOLR_COLLECTION
from pysolr import Solr

bp = Blueprint("api", __name__, url_prefix="/api/v1")
solr = Solr(SOLR_COLLECTION)


@bp.route("/counter", methods=["GET"])
def index():
    legal_reforms_and_policies = solr.search("*:*", **{"rows": 0, "wt": "json", "fq": COUNTER_QUERIES["legal_reforms_and_policies"]})
    medication_assisted_treatment = solr.search("*:*", **{"rows": 0, "wt": "json", "fq": COUNTER_QUERIES["medication_assisted_treatment"]})
    overdose_prevention_and_response = solr.search("*:*", **{"rows": 0, "wt": "json", "fq": COUNTER_QUERIES["overdose_prevention_and_response"]})
    prevention_and_education = solr.search("*:*", **{"rows": 0, "wt": "json", "fq": COUNTER_QUERIES["prevention_and_education"]})
    psychosocial_therapy = solr.search("*:*", **{"rows": 0, "wt": "json", "fq": COUNTER_QUERIES["psychosocial_therapy"]})
    safe_prescribing = solr.search("*:*", **{"rows": 0, "wt": "json", "fq": COUNTER_QUERIES["safe_prescribing"]})
    treatment_delivery_models = solr.search("*:*", **{"rows": 0, "wt": "json", "fq": COUNTER_QUERIES["treatment_delivery_models"]})
    return jsonify({"legal_reforms_and_policies": legal_reforms_and_policies.hits,
                    "medication_assisted_treatment": medication_assisted_treatment.hits,
                    "overdose_prevention_and_response": overdose_prevention_and_response.hits,
                    "prevention_and_education": prevention_and_education.hits,
                    "psychosocial_therapy": psychosocial_therapy.hits,
                    "safe_prescribing": safe_prescribing.hits,
                    "treatment_delivery_models": treatment_delivery_models.hits})
