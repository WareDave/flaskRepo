import os
from flask import Flask, jsonify, g
from flask_cors import CORS
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = 'ballsdeep'
login_manager = LoginManager()
login_manager.init_app(app)

import models
from resources.character import characters
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

from resources.user import users
from resources.character import characters


CORS(users, origins=['http://localhost:3000'], supports_credentials=True)
CORS(characters, origins=['http://localhost:3000'], supports_credentials=True)



@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()

app.register_blueprint(users, url_prefix='/api/v1/users')
app.register_blueprint(characters, url_prefix='/api/v1/characters')


@app.after_request
def after_request(response):
    g.db.close()
    return response

@app.route('/')
def index():
    return 'hi'

DEBUG = True
PORT = 8000
if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)