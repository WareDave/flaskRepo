from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required

import models

waitlists = Blueprint('waitlists', 'waitlists')
print()

# Index route
@waitlist.route('/', methods=["GET"])
def get_all_waitlists():
    try:
        waitlists = [model_to_dict(waitlist) for waitlist in models.WaitList.select().where(models.WaitList.loggedUser_id == current_user.id)]
        print(waitlists)
        for waitlist in waitlists:
            waitlist['loggedUser'].pop('password')
        return jsonify(data=waitlists, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 400, "message": "Error getting the resources"})

# Create route
@waitlist.route('/', methods=["POST"])
@login_required
def create_waitlists():
    try:
        payload = request.get_json()
        payload['loggedUser'] = current_user.id
        waitlist = models.WaitList.create(**payload)
        print(waitlist.__dict__)
        waitlist_dict = model_to_dict(waitlist)

        return jsonify(data = waitlist_dict, status = {"code": 201, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 400, "message": "Error creating the resources"})


# Show route
@waitlist.route('/<id>', methods=["GET"])
def get_one_waitlists(id):
    try:
        waitlist = models.WaitList.get_by_id(id)
        print(waitlist)
        waitlist_dict = model_to_dict(waitlist)
        return jsonify(data = waitlist_dict, status={"code": 200, "message": f"Found waitlist with id {waitlist.id}"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 400, "message": "Error getting one resource"})

# Update route
@waitlist.route('/<id>', methods=["PUT"])
def update_waitlists(id):
    try:
        payload = request.get_json()
        query = models.WaitList.update(**payload).where(models.WaitList.id == id)
        query.execute()
        updated_waitlist = model_to_dict(models.WaitList.get_by_id(id))
        return jsonify(data=updated_waitlist, status={"code": 200, "message": f"Resourced updated successfully"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 400, "message": "Error updating one resource"})


# Delete route
@waitlist.route('/<id>', methods=["DELETE"])
def delete_waitlist(id):
    try:
        query = models.WaitList.delete().where(models.WaitList.id == id)
        query.execute()
        return jsonify(data='Resource successfully deleted', status={"code": 200, "message": "Resource successfully deleted"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 400, "message": "Error deleting resource"})
