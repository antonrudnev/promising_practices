from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

import admin, api, auth, db, demo, practice, workspace


app = Flask(__name__)
app.register_blueprint(admin.bp)
app.register_blueprint(auth.bp)
app.register_blueprint(workspace.bp)
app.register_blueprint(practice.bp)
app.register_blueprint(api.bp)
app.register_blueprint(demo.bp)
app.add_url_rule("/", endpoint="/practice/index/", view_func=practice.index)
app.config.from_pyfile("settings.py")
app.wsgi_app = ProxyFix(app.wsgi_app)
db.init_app(app)


if __name__ == "__main__":
    app.run()
