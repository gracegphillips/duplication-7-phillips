from flask import Flask, g
from .app_factory import create_app
from .db_connect import get_db, close_db

app = create_app()
app.secret_key = 'your-secret'

from app.blueprints.clients import clients
app.register_blueprint(clients)

from app.blueprints.properties import properties
app.register_blueprint(properties)


from . import routes

@app.before_request
def before_request():
    g.db = get_db()

# Setup database connection teardown
@app.teardown_appcontext
def teardown_db(exception=None):
    close_db(exception)