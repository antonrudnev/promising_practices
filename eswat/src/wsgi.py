from werkzeug.exceptions import NotFound
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from app import app

wsgi_app = DispatcherMiddleware(NotFound(), {"/eswat": app})


if __name__ == "__main__":
    app.run()
