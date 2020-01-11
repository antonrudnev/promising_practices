from auth import login_required
from db import get_mentions, get_users, delete_mention
from flask import Blueprint, flash, g, redirect, render_template, url_for
import functools

bp = Blueprint("workspace", __name__, url_prefix="/workspace/")


def push_mentions(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        cnt = len([x for x in get_mentions(g.user["id"]) if x["was_read"] == 0])
        if cnt > 0:
            flash({"status": "alert-info", "text": "You have been mentioned in {} discussion(s) recently.".format(cnt)})
        return view(**kwargs)
    return wrapped_view


@bp.route("/workflow/", methods=["GET"])
@login_required
def workflow():
    return render_template("workspace/workflow.html")


@bp.route("/team/", methods=["GET"])
@login_required
def team():
    users = [x for x in get_users() if x["is_enabled"] == 1 and x["user_name"] != "admin"]
    return render_template("workspace/team.html", users=users)


@bp.route("/threads/", methods=["GET"])
@login_required
def threads():
    mentions = get_mentions(g.user["id"])
    return render_template("workspace/threads.html", mentions=mentions)


@bp.route("/dismiss/<int:id>/", methods=["GET"])
@login_required
def dismiss(id):
    delete_mention(g.user["id"], id)
    return redirect(url_for("workspace.threads"))
