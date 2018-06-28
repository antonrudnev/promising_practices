from flask import Flask

import admin
import auth
import practice
from db import close_db

app = Flask(__name__)
app.register_blueprint(admin.bp)
app.register_blueprint(auth.bp)
app.register_blueprint(practice.bp)
app.add_url_rule("/", endpoint="practice", view_func=practice.index)
app.config.from_mapping(SECRET_KEY="dev")
app.teardown_appcontext(close_db)


if __name__ == "__main__":
    app.run()
