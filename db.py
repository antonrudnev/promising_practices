from flask import g
from settings import DIRECTORY_DATABASE
import sqlite3
from werkzeug.security import generate_password_hash


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DIRECTORY_DATABASE, detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    with sqlite3.connect(DIRECTORY_DATABASE, detect_types=sqlite3.PARSE_DECLTYPES) as db:
        db.row_factory = sqlite3.Row
        with open("schema.sql") as f:
            db.executescript(f.read())
        print("Initialized the database.")
        for user in db.execute("SELECT id, password FROM user"):
            db.execute("UPDATE user SET password = ? WHERE id = ?",
                       (generate_password_hash(user["password"]), user["id"]))
        db.commit()
        print("Initialized the content.")


if __name__ == "__main__":
    init_db()
