from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required

import models

legals = Blueprint('legals', 'legals')
print()

# Index route
@legals.route('/', methods=["GET"])
def get_all_legals():
    try:
        legals = [model_to_dict(legal) for legal in models.Legal.select().where(models.Legal.loggedUser_id == current_user.id)]
        print(legals)
        for legal in legals:
            legal['loggedUser'].pop('password')
        return jsonify(data=legals, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 400, "message": "Error getting the resources"})

# Create route
@legals.route('/', methods=["POST"])
@login_required
def create_legals():
    try:
        payload = request.get_json()
        payload['loggedUser'] = current_user.id
        legal = models.Legal.create(**payload)
        print(legal.__dict__)
        legal_dict = model_to_dict(legal)

        return jsonify(data = legal_dict, status = {"code": 201, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 400, "message": "Error creating the resources"})


# Show route
@legals.route('/<id>', methods=["GET"])
def get_one_legals(id):
    try:
        legal = models.Legal.get_by_id(id)
        print(legal)
        legal_dict = model_to_dict(legal)
        return jsonify(data = legal_dict, status={"code": 200, "message": f"Found legal with id {legal.id}"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 400, "message": "Error getting one resource"})

# Update route
@legals.route('/<id>', methods=["PUT"])
def update_legals(id):
    try:
        payload = request.get_json()
        query = models.Legal.update(**payload).where(models.Legal.id == id)
        query.execute()
        updated_legal = model_to_dict(models.Legal.get_by_id(id))
        return jsonify(data=updated_legal, status={"code": 200, "message": f"Resourced updated successfully"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 400, "message": "Error updating one resource"})


# Delete route
@legals.route('/<id>', methods=["DELETE"])
def delete_legal(id):
    try:
        query = models.Legal.delete().where(models.Legal.id == id)
        query.execute()
        return jsonify(data='Resource successfully deleted', status={"code": 200, "message": "Resource successfully deleted"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 400, "message": "Error deleting resource"})
