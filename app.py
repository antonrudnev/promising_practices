from db import close_db
from flask import Flask
import practice

app = Flask(__name__)
app.register_blueprint(practice.bp)
app.add_url_rule("/", endpoint="practice", view_func=practice.index)
app.config.from_mapping(SECRET_KEY="dev")
app.teardown_appcontext(close_db)


if __name__ == "__main__":
    app.run()
