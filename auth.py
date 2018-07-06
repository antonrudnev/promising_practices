import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from db import get_db
from werkzeug.security import check_password_hash, generate_password_hash


bp = Blueprint("auth", __name__, url_prefix="/auth")


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        db = get_db()
        db.execute("UPDATE user SET last_login = CURRENT_TIMESTAMP WHERE id = ?", (g.user["id"],))
        db.commit()
        return view(**kwargs)
    return wrapped_view


def permission_required(permission, rule=None):
    def security_decorator(view):
        @functools.wraps(view)
        def wrapped_view(**kwargs):
            if rule == "status_based":
                p = permission + "_" + g.document["status"]
            elif rule == "action_based":
                action = request.form["action"].upper()
                p = permission + "_" + action
            else:
                p = permission
            if p not in g.permissions:
                flash({"status": "alert-danger", "text": "You don't have permission to perform this operation. "
                                                         "Access is denied."})
                return redirect(url_for("practice.index"))
            return view(**kwargs)
        return wrapped_view
    return security_decorator


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
        permissions = get_db().execute("SELECT DISTINCT permission_name FROM user_role "
                                       "JOIN role_permission ON user_role.role_id = role_permission.role_id "
                                       "JOIN permission ON role_permission.permission_id = permission.id "
                                       "WHERE user_role.user_id = ?", (user_id,)).fetchall()
        g.permissions = [p["permission_name"] for p in permissions]


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        fullname = request.form["fullname"].strip()
        password = request.form["password"]
        db = get_db()
        error = None

        if not username:
            error = "Username is required."
        elif not fullname:
            error = "Full name is required."
        elif not password:
            error = "Password is required."
        elif db.execute("SELECT id FROM user WHERE user_name = ?", (username,)).fetchone() is not None:
            error = "User {0} is already registered.".format(username)

        if error is None:
            db.execute("INSERT INTO user (user_name, full_name, password) VALUES (?, ?, ?)",
                       (username, fullname, generate_password_hash(password)))
            db.commit()
            flash({"status": "alert-success", "text": "You have successfully registered."})
            return redirect(url_for("auth.login"))

        flash({"status": "alert-danger", "text": error})

    return render_template("auth/register.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        password = request.form["password"]
        db = get_db()
        error = None
        user = db.execute("SELECT * FROM user WHERE user_name = ?", (username,)).fetchone()

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password."
        elif not user["enabled"]:
            error = "You account is disabled."

        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("practice.index"))

        flash({"status": "alert-danger", "text": error})

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("practice.index"))
