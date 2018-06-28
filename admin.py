from auth import login_required, permission_required
from db import get_db
from flask import Blueprint, render_template

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/workflow", methods=["GET"])
@login_required
def workflow():
    return render_template("admin/workflow.html")


@bp.route("/users", methods=["GET"])
@login_required
@permission_required("SECURITY_ADMIN")
def users():
    users_tbl = get_db().execute("SELECT T.user_name, "
                                 "T.full_name, "
                                 "T.enabled, "
                                 "IFNULL(GROUP_CONCAT(role_name), '') AS roles "
                                 "FROM (SELECT user_name, "
                                 "full_name, "
                                 "enabled, "
                                 "role_name FROM user "
                                 "LEFT JOIN user_role ON user.id = user_role.user_id "
                                 "LEFT JOIN role ON user_role.role_id = role.id) AS T "
                                 "GROUP BY user_name, full_name, enabled "
                                 "ORDER BY user_name").fetchall()

    users = [{"user_name": user["user_name"],
              "full_name": user["full_name"],
              "enabled": user["enabled"],
              "roles": user["roles"].split(",")} for user in users_tbl]

    return render_template("admin/users.html", users=users)


@bp.route("/roles", methods=["GET"])
@login_required
@permission_required("SECURITY_ADMIN")
def roles():
    roles_tbl = get_db().execute("SELECT T.role_name, "
                                 "IFNULL(GROUP_CONCAT(permission_name), '') AS permissions, "
                                 "IFNULL(GROUP_CONCAT(enabled), '') AS enabled_list "
                                 "FROM (SELECT role_name,"
                                 "permission_name,"
                                 "CASE WHEN role_id ISNULL THEN 0 ELSE 1 END AS enabled "
                                 "FROM role CROSS JOIN permission "
                                 "LEFT JOIN role_permission ON role.id = role_permission.role_id "
                                 "AND permission.id = role_permission.permission_id "
                                 "ORDER BY role_name, permission_name) AS T GROUP BY role_name").fetchall()

    roles = [{"role_name": role["role_name"],
              "permissions": role["permissions"].split(","),
              "enabled_list": role["enabled_list"].split(",")} for role in roles_tbl]

    return render_template("admin/roles.html", roles=roles)
