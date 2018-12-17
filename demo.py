from auth import login_required, permission_required
from db import delete_demo_request, get_demo_request, get_demo_requests, read_demo_request
from flask import Blueprint, redirect, render_template, url_for

bp = Blueprint('demo', __name__, url_prefix="/demo")


@bp.route("/", methods=["GET"])
@login_required
@permission_required("ADMIN_DEMOREQUESTS")
def index():
    demo_requests = get_demo_requests()
    return render_template("demo/index.html", demo_requests=demo_requests)


@bp.route("/<int:demo_request_id>", methods=["GET"])
@login_required
@permission_required("ADMIN_DEMOREQUESTS")
def details(demo_request_id):
    demo_request = get_demo_request(demo_request_id)
    read_demo_request(demo_request_id)
    return render_template("demo/details.html", demo_request=demo_request)


@bp.route("/<int:demo_request_id>/delete", methods=["POST"])
@login_required
@permission_required("ADMIN_DEMOREQUESTS")
def delete(demo_request_id):
    delete_demo_request(demo_request_id)
    return redirect(url_for("demo.index"))
