from auth import login_required, permission_required
from db import get_db, get_roles, get_users, update_users_roles, update_roles_permissions
from flask import Blueprint, flash, render_template, request

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/users", methods=["GET", "POST"])
@login_required
@permission_required("SECURITY_ADMIN")
def users():
    if request.method == "POST":
        assigned = request.form.getlist("assigned")
        enabled = request.form.getlist("enabled")
        update_users_roles(assigned, enabled)
        flash({"status": "alert-success", "text": "Security changes have been successfully applied."})
    users = get_users()
    return render_template("admin/users.html", users=users)


@bp.route("/roles", methods=["GET", "POST"])
@login_required
@permission_required("SECURITY_ADMIN")
def roles():
    if request.method == "POST":
        assigned = request.form.getlist("assigned")
        update_roles_permissions(assigned)
        flash({"status": "alert-success", "text": "Security changes have been successfully applied."})
    roles = get_roles()
    return render_template("admin/roles.html", roles=roles)
