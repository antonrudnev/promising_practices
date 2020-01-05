from flask import Flask
from werkzeug.contrib.fixers import ProxyFix

import admin
import api
import auth
import db
import demo
import practice
import workspace


app = Flask(__name__)
app.register_blueprint(admin.bp, url_prefix="/eswat/admin")
app.register_blueprint(auth.bp, url_prefix="/eswat/auth")
app.register_blueprint(workspace.bp, url_prefix="/eswat/workspace")
app.register_blueprint(practice.bp, url_prefix="/eswat/practice")
app.register_blueprint(api.bp)
app.register_blueprint(demo.bp, url_prefix="/eswat/demo")
app.add_url_rule("/eswat", endpoint="/eswat/practice", view_func=practice.index)
app.config.from_mapping(SECRET_KEY="fj5kqkdf9r")
app.config.from_pyfile("settings.py")
app.wsgi_app = ProxyFix(app.wsgi_app)
db.init_app(app)


if __name__ == "__main__":
    app.run()
