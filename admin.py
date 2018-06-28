from auth import login_required, permission_required
from db import get_db
from flask import Blueprint, flash, render_template, request

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/workflow", methods=["GET"])
@login_required
def workflow():
    return render_template("admin/workflow.html")


@bp.route("/users", methods=["GET", "POST"])
@login_required
@permission_required("SECURITY_ADMIN")
def users():
    if request.method == "POST":
        assigned = request.form.getlist("assigned")
        print(assigned)
        db = get_db()
        db.execute("DELETE FROM user_role")
        for a in assigned:
            user_role = a.split(",")
            db.execute("INSERT INTO user_role (user_id, role_id) VALUES (?, ?)", (user_role[0], user_role[1]))
        db.commit()
        flash({"status": "alert-success", "text": "Security changes have been successfully applied."})
    users_tbl = get_db().execute("SELECT user_id, "
                                 "user_name, "
                                 "full_name, "
                                 "enabled, "
                                 "IFNULL(GROUP_CONCAT(role_id), '') AS role_ids ,"
                                 "IFNULL(GROUP_CONCAT(role_name), '') AS roles ,"
                                 "IFNULL(GROUP_CONCAT(assigned), '') AS assigned "
                                 "FROM (SELECT user.id AS user_id, "
                                 "user_name, "
                                 "full_name, "
                                 "enabled, "
                                 "role.id AS role_id, "
                                 "role_name, "
                                 "CASE WHEN role_id ISNULL THEN 0 ELSE 1 END AS assigned "
                                 "FROM user "
                                 "CROSS JOIN role "
                                 "LEFT JOIN user_role ON user.id = user_role.user_id "
                                 "AND role.id = user_role.role_id "
                                 "ORDER BY user_name, role_name)"
                                 "GROUP BY user_id, user_name, full_name, enabled "
                                 "ORDER BY user_name").fetchall()

    users = [{"user_id": str(user["user_id"]),
              "user_name": user["user_name"],
              "full_name": user["full_name"],
              "enabled": user["enabled"],
              "roles": user["roles"].split(","),
              "assigned": zip(user["role_ids"].split(","), user["assigned"].split(","))} for user in users_tbl]

    return render_template("admin/users.html", users=users)


@bp.route("/roles", methods=["GET"])
@login_required
@permission_required("SECURITY_ADMIN")
def roles():
    roles_tbl = get_db().execute("SELECT role_name, "
                                 "IFNULL(GROUP_CONCAT(permission_name), '') AS permissions, "
                                 "IFNULL(GROUP_CONCAT(assigned), '') AS assigned "
                                 "FROM (SELECT role_name,"
                                 "permission_name,"
                                 "CASE WHEN role_id ISNULL THEN 0 ELSE 1 END AS assigned "
                                 "FROM role "
                                 "CROSS JOIN permission "
                                 "LEFT JOIN role_permission ON role.id = role_permission.role_id "
                                 "AND permission.id = role_permission.permission_id "
                                 "ORDER BY role_name, permission_name) "
                                 "GROUP BY role_name "
                                 "ORDER BY role_name, permission_name").fetchall()

    roles = [{"role_name": role["role_name"],
              "permissions": role["permissions"].split(","),
              "assigned": role["assigned"].split(",")} for role in roles_tbl]

    return render_template("admin/roles.html", roles=roles)
