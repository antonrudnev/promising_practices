from flask import g
from settings import SYSTEM_DATABASE
import sqlite3
from werkzeug.security import generate_password_hash


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(SYSTEM_DATABASE, detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    with sqlite3.connect(SYSTEM_DATABASE, detect_types=sqlite3.PARSE_DECLTYPES) as db:
        db.row_factory = sqlite3.Row
        with open("schema.sql") as f:
            db.executescript(f.read())
        print("Initialized the database.")
        for user in db.execute("SELECT id, password FROM user"):
            db.execute("UPDATE user SET password = ? WHERE id = ?",
                       (generate_password_hash(user["password"]), user["id"]))
        db.commit()
        print("Initialized the content.")


def get_comments(document_id):
    db = get_db()
    return db.execute("SELECT user_comment.id, "
                      "user_comment.user_id, "
                      "user.user_name, "
                      "user.full_name, "
                      "user_comment.comment, "
                      "user_comment.created_on "
                      "FROM user_comment "
                      "JOIN user ON user.id = user_comment.user_id "
                      "WHERE document_id = ? "
                      "ORDER BY user_comment.created_on", (document_id,)).fetchall()


def delete_comments(document_id):
    db = get_db()
    db.execute("DELETE FROM user_mention "
               "WHERE user_comment_id in (SELECT id FROM user_comment WHERE document_id = ?)", (document_id,))
    db.execute("DELETE FROM user_comment "
               "WHERE document_id = ? ", (document_id,))
    db.commit()


def get_mentions(user_id):
    db = get_db()
    return db.execute("SELECT user_comment.document_id, "
                      "user_comment.comment, "
                      "user_comment.created_on, "
                      "user_mention.was_read, "
                      "user.full_name "
                      "FROM user_comment "
                      "JOIN (SELECT user_comment.document_id, "
                      "MAX(user_mention.user_comment_id) AS user_comment_id "
                      "FROM user_mention "
                      "JOIN user_comment on user_mention.user_comment_id = user_comment.id "
                      "WHERE user_mention.user_id = ? AND NOT user_mention.was_deleted "
                      "GROUP BY user_comment.document_id) AS T ON T.user_comment_id = user_comment.id "
                      "JOIN user ON user.id = user_comment.user_id "
                      "JOIN user_mention ON user_mention.user_id = ? "
                      "AND user_mention.user_comment_id = user_comment.id "
                      "ORDER BY user_mention.was_read, user_comment.created_on DESC", (user_id, user_id)).fetchall()


def read_mention(user_id, document_id):
    db = get_db()
    db.execute("UPDATE user_mention "
               "SET was_read = 1 "
               "WHERE user_id = ? AND EXISTS(SELECT * FROM user_comment "
               "WHERE user_comment.id = user_mention.user_comment_id AND user_comment.document_id = ?)",
               (user_id, document_id))
    db.commit()


def delete_mention(user_id, document_id):
    db = get_db()
    db.execute("UPDATE user_mention "
               "SET was_deleted = 1 "
               "WHERE user_id = ? AND EXISTS(SELECT * FROM user_comment "
               "WHERE user_comment.id = user_mention.user_comment_id AND user_comment.document_id = ?)",
               (user_id, document_id))
    db.commit()


def insert_comment(document_id, user_id, comment):
    if not comment.strip():
        return
    db = get_db()
    cur = db.cursor()
    users = cur.execute("SELECT id, user_name FROM user").fetchall()
    mentions = [g.user["id"]]
    for user in users:
        if "@" + user["user_name"] in comment:
            comment = comment.replace("@" + user["user_name"], "<mark>@" + user["user_name"] + "</mark>")
            if user["id"] != g.user["id"]:
                mentions.append(user["id"])
    comment = comment.replace("\n", "<br>")
    cur.execute("INSERT INTO user_comment (document_id, user_id, comment) VALUES (?, ?, ?)",
                (document_id, user_id, comment))
    comment_id = cur.lastrowid

    for user_id in mentions:
        cur.execute("INSERT INTO user_mention (user_id, user_comment_id, was_read) VALUES (?, ?, ?)",
                    (user_id, comment_id, user_id == g.user["id"]))
    db.commit()


def get_users():
    db = get_db()
    users_tbl = db.execute("SELECT user_id, "
                           "user_name, "
                           "full_name, "
                           "is_enabled, "
                           "created_on, "
                           "last_login, "
                           "IFNULL(GROUP_CONCAT(role_id), '') AS role_ids ,"
                           "IFNULL(GROUP_CONCAT(role_name), '') AS roles ,"
                           "IFNULL(GROUP_CONCAT(assigned), '') AS assigned "
                           "FROM (SELECT user.id AS user_id, "
                           "user.user_name, "
                           "user.full_name, "
                           "user.is_enabled, "
                           "user.created_on, "
                           "user.last_login, "
                           "role.id AS role_id, "
                           "role.role_name, "
                           "CASE WHEN role_id ISNULL THEN 0 ELSE 1 END AS assigned "
                           "FROM user "
                           "CROSS JOIN role "
                           "LEFT JOIN user_role ON user.id = user_role.user_id "
                           "AND role.id = user_role.role_id "
                           "ORDER BY user.user_name, role.role_name)"
                           "GROUP BY user_id, user_name, full_name, is_enabled, created_on, last_login "
                           "ORDER BY user_name").fetchall()

    return [{"user_id": str(user["user_id"]),
             "user_name": user["user_name"],
             "full_name": user["full_name"],
             "is_enabled": user["is_enabled"],
             "created_on": user["created_on"],
             "last_login": user["last_login"],
             "roles": list(zip(user["role_ids"].split(","),
                               user["roles"].split(","),
                               user["assigned"].split(",")))} for user in users_tbl]


def update_users_roles(assigned, enabled):
    db = get_db()
    db.execute("DELETE FROM user_role")
    db.execute("INSERT INTO user_role (user_id, role_id) "
               "SELECT user.id, role.id FROM user "
               "JOIN role ON user_name = 'admin' "
               "AND role_name = 'administrator'")
    db.execute("UPDATE user SET is_enabled = 0 WHERE id != ?", (g.user["id"],))
    for a in assigned:
        user_role = a.split(",")
        db.execute("INSERT INTO user_role (user_id, role_id) VALUES (?, ?)", (user_role[0], user_role[1]))
    for e in enabled:
        db.execute("UPDATE user SET is_enabled = 1 WHERE id = ?", (e,))
    db.commit()


def update_roles_permissions(assigned):
    db = get_db()
    db.execute("DELETE FROM role_permission")
    db.execute("INSERT INTO role_permission (role_id, permission_id) "
               "SELECT role.id, permission.id FROM role "
               "JOIN permission ON role_name = 'administrator' "
               "AND permission_name LIKE 'ADMIN_%'")
    for a in assigned:
        role_permission = a.split(",")
        db.execute("INSERT INTO role_permission (role_id, permission_id) VALUES (?, ?)",
                   (role_permission[0], role_permission[1]))
    db.commit()


def get_roles():
    db = get_db()
    roles_tbl = db.execute("SELECT role_id, "
                           "role_name, "
                           "IFNULL(GROUP_CONCAT(permission_id), '') AS permission_ids ,"
                           "IFNULL(GROUP_CONCAT(permission_name), '') AS permissions, "
                           "IFNULL(GROUP_CONCAT(assigned), '') AS assigned "
                           "FROM (SELECT role.id AS role_id, "
                           "permission.id AS permission_id, "                           
                           "role.role_name,"
                           "permission.permission_name,"
                           "CASE WHEN role_permission.role_id ISNULL THEN 0 ELSE 1 END AS assigned "
                           "FROM role "
                           "CROSS JOIN permission "
                           "LEFT JOIN role_permission ON role.id = role_permission.role_id "
                           "AND permission.id = role_permission.permission_id "
                           "ORDER BY role.role_name, permission.permission_name) "
                           "GROUP BY role_id, role_name "
                           "ORDER BY role_name").fetchall()

    return [{"role_id": str(role["role_id"]),
             "role_name": role["role_name"],
             "permissions": list(zip(role["permission_ids"].split(","),
                                     role["permissions"].split(","),
                                     role["assigned"].split(",")))} for role in roles_tbl]


if __name__ == "__main__":
    init_db()
