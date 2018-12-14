from flask import Flask

import admin
import api
import auth
import db
import demo
import practice
import workspace


app = Flask(__name__)
app.register_blueprint(admin.bp)
app.register_blueprint(auth.bp)
app.register_blueprint(workspace.bp)
app.register_blueprint(practice.bp)
app.register_blueprint(api.bp)
app.register_blueprint(demo.bp)
app.add_url_rule("/", endpoint="practice", view_func=practice.index)
app.config.from_mapping(SECRET_KEY="dev")
app.config.from_pyfile("settings.py")
db.init_app(app)


if __name__ == "__main__":
    app.run()
