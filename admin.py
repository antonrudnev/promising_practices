from auth import login_required, permission_required
from db import get_db, get_roles, get_users
from flask import Blueprint, flash, render_template, request

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/users", methods=["GET", "POST"])
@login_required
@permission_required("SECURITY_ADMIN")
def users():
    if request.method == "POST":
        assigned = request.form.getlist("assigned")
        enabled = request.form.getlist("enabled")
        db = get_db()
        db.execute("DELETE FROM user_role")
        db.execute("INSERT INTO user_role (user_id, role_id) "
                   "SELECT user.id, role.id FROM user "
                   "JOIN role ON user_name='admin' "
                   "AND role_name='administrator'")
        db.execute("UPDATE user SET is_enabled = 0 WHERE user_name != 'admin'")
        for a in assigned:
            user_role = a.split(",")
            db.execute("INSERT INTO user_role (user_id, role_id) VALUES (?, ?)", (user_role[0], user_role[1]))
        for e in enabled:
            db.execute("UPDATE user SET is_enabled = 1 WHERE id = ?", (e,))
        db.commit()
        flash({"status": "alert-success", "text": "Security changes have been successfully applied."})

    users = get_users()
    return render_template("admin/users.html", users=users)


@bp.route("/roles", methods=["GET"])
@login_required
@permission_required("SECURITY_ADMIN")
def roles():
    roles = get_roles()
    return render_template("admin/roles.html", roles=roles)
