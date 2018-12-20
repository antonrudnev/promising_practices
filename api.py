from flask import abort, Blueprint, jsonify, request
from db import insert_demo_request
from settings import COUNTER_QUERIES, SOLR_COLLECTION
from pysolr import Solr
from settings import CORRD_MANAGER_BOT
from telegram import Bot
from telegram.error import TelegramError

import json

bp = Blueprint("api", __name__, url_prefix="/api/v1")
solr = Solr(SOLR_COLLECTION)


def push_notification(message):
    bot = Bot(CORRD_MANAGER_BOT)
    try:
        bot.sendMessage(chat_id=-1001347417582, text=message)
    except TelegramError:
        pass


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
        request_details["remote_addr"] = request.remote_addr
        insert_demo_request(json.dumps(request_details))
        push_notification(
            f'A new demo request from {request_details["first_name"]} {request_details["last_name"]} '
            f'({request_details["organization_name"]}) was received.')
        return jsonify("Request received"), 201
    except Exception:
        push_notification(
            "An attempt to send a demo request was made and failed. Please check if ESWAT API works properly. ")
        return abort(500)
