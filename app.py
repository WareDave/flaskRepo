import os
from flask import Flask, jsonify, g
from flask_cors import CORS
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = 'BallsDeep'
login_manager = LoginManager()
login_manager.init_app(app)

import models
from resources.character import stocks
from resources.user import users

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None

@login_manager.unauthorized_handler
def unauthorized():
    return jsonify(
        data = {
            'error': 'User not logged in.'
        },
        status = {
            'code': 401,
            'message': 'You must be logged in to access that resource.'
        }
    )



CORS(users, origins=['http://localhost:3000'], supports_credentials=True)
CORS(stocks, origins=['http://localhost:3000'], supports_credentials=True)
CORS(legals, origins=['http://localhost:3000'], supports_credentials=True)


@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()

app.register_blueprint(users, url_prefix='/api/v1/users')
app.register_blueprint(stocks, url_prefix='/api/v1/stocks')
app.register_blueprint(legals, url_prefix='/api/v1/legals')


@app.after_request
def after_request(response):
    g.db.close()
    return response

@app.route('/')
def index():
    return 'Fuck You'


DEBUG = True
PORT = 8000
if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)