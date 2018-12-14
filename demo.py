from auth import login_required, permission_required
from db import get_demo_requests
from flask import Blueprint, render_template

bp = Blueprint('demo', __name__, url_prefix="/demo")


@bp.route("/", methods=["GET"])
@login_required
@permission_required("ADMIN_DEMOREQUESTS")
def index():
    requests = get_demo_requests()
    return render_template("demo/index.html", requests=requests)
