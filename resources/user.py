from flask import request, jsonify, Blueprint
from playhouse.shortcuts import model_to_dict
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user

import models

users = Blueprint('users', 'users')


@users.route('/register', methods = ['POST'])
def register():
    payload = request.get_json()
    payload['email'].lower()

    try:
        models.User.get(models.User.email == payload['email'])

        return jsonify(data={}, status={"code": 400, "message": "Used E-Mail! already exists. Go login"})

    except models.DoesNotExist:
        payload['password'] = generate_password_hash(payload['password'])
        print(payload)
        user = models.User.create(**payload)
        login_user(user)
        user_dict = model_to_dict(user)

        del user_dict['password']
        return jsonify(data = user_dict, status = {'code': 200, 'message': f"Successfully registered let us adventure {user_dict['email']}"})


@users.route('/login', methods=['POST'])
def login():
    payload = request.get_json()
    payload['email'].lower()

    try:
        user = models.User.get(models.User.email == payload['email'])

        user_dict = model_to_dict(user)

       
        if(check_password_hash(user_dict['password'], payload['password'])):
            del user_dict['password']
            login_user(user)
            return jsonify(data = user_dict, status = {'code': 200, 'message': f"You Son Of A Bitch, I'm In! {user_dict['email']}"})
        
        else:
            return jsonify(data={}, status = {'code': 401, 'message': 'Uh, Your Shit Is Like All Retarded'})

    except models.DoesNotExist:
        return jsonify(data={}, status = {'code': 401, 'message': 'You Done Fucked Up. Try Again.'})

@users.route('/logout', methods = ['GET'])
def logout():
    email = model_to_dict(current_user)['email']

    logout_user()

    return jsonify(data={}, status = { 'code': 200, 'message': f"Successfully logged out {email}"})

