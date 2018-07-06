from auth import login_required
from db import get_mentions
from flask import Blueprint, flash, g, render_template
import functools

bp = Blueprint("workspace", __name__, url_prefix="/workspace")


def push_mentions(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        cnt = len([x for x in get_mentions(g.user["id"]) if x["was_read"] == 0])
        if cnt > 0:
            flash({"status": "alert-info", "text": "You have been mentioned in {} discussion(s) recently.".format(cnt)})
        return view(**kwargs)
    return wrapped_view


@bp.route("/workflow", methods=["GET"])
@login_required
def workflow():
    return render_template("workspace/workflow.html")


@bp.route("/threads", methods=["GET"])
@login_required
def threads():
    mentions = get_mentions(g.user["id"])
    return render_template("workspace/threads.html", mentions=mentions)
