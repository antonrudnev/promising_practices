from auth import login_required
from flask import Blueprint, render_template

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/workflow", methods=["GET"])
@login_required
def workflow():
    return render_template("workflow.html")
