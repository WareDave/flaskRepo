from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required

import models

characters = Blueprint('characters', 'characters')
print()

# Index route
@characters.route('/', methods=["GET"])
def get_all_characters():
    try:
        characters = [model_to_dict(character) for character in models.Character.select().where(models.Character.loggedUser_id == current_user.id)]
        print(characters)
        for character in characters:
            character['loggedUser_id'].pop('password')
        return jsonify(data=characters, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 400, "message": "Error getting the resources"})

# Create route
@characters.route('/', methods=["POST"])
@login_required
def create_characters():
    try:
        payload = request.get_json()
        payload['loggedUser'] = current_user.id
        character = models.Character.create(**payload)
        print(character.__dict__)
        character_dict = model_to_dict(character)

        return jsonify(data = character_dict, status = {"code": 201, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 400, "message": "Error creating the resources"})


# Show route
@characters.route('/<id>', methods=["GET"])
def get_one_characters(id):
    try:
        character = models.Character.get_by_id(id)
        print(character)
        character_dict = model_to_dict(character)
        return jsonify(data = character_dict, status={"code": 200, "message": f"Found character with id {character.id}"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 400, "message": "Error getting one resource"})

# Update route
@characters.route('/<id>', methods=["PUT"])
def update_characters(id):
    try:
        payload = request.get_json()
        query = models.Character.update(**payload).where(models.Character.id == id)
        query.execute()
        updated_character = model_to_dict(models.Character.get_by_id(id))
        return jsonify(data=updated_character, status={"code": 200, "message": f"Resourced updated successfully"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 400, "message": "Error updating one resource"})


# Delete route
@characters.route('/<id>', methods=["DELETE"])
def delete_character(id):
    try:
        query = models.Character.delete().where(models.Character.id == id)
        query.execute()
        return jsonify(data='Resource successfully deleted', status={"code": 200, "message": "Resource successfully deleted"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 400, "message": "Error deleting resource"})
