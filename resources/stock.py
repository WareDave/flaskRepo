from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
from flask_login import current_user, login_required

import models

stocks = Blueprint('stocks', 'stocks')
print()

# Index route
@stocks.route('/', methods=["GET"])
def get_all_stocks():
    try:
        stocks = [model_to_dict(stock) for stock in models.Stock.select().where(models.Stock.loggedUser_id == current_user.id)]
        print(stocks)
        for stock in stocks:
            stock['loggedUser'].pop('password')
        return jsonify(data=stocks, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 400, "message": "Error getting the resources"})

# Create route
@stocks.route('/', methods=["POST"])
@login_required
def create_stocks():
    try:
        payload = request.get_json()
        payload['loggedUser'] = current_user.id
        stock = models.Stock.create(**payload)
        print(stock.__dict__)
        stock_dict = model_to_dict(stock)

        return jsonify(data = stock_dict, status = {"code": 201, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 400, "message": "Error creating the resources"})


# Show route
@stocks.route('/<id>', methods=["GET"])
def get_one_stocks(id):
    try:
        stock = models.Stock.get_by_id(id)
        print(stock)
        stock_dict = model_to_dict(stock)
        return jsonify(data = stock_dict, status={"code": 200, "message": f"Found stock with id {stock.id}"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 400, "message": "Error getting one resource"})

# Update route
@stocks.route('/<id>', methods=["PUT"])
def update_stocks(id):
    try:
        payload = request.get_json()
        query = models.Stock.update(**payload).where(models.Stock.id == id)
        query.execute()
        updated_stock = model_to_dict(models.Stock.get_by_id(id))
        return jsonify(data=updated_stock, status={"code": 200, "message": f"Resourced updated successfully"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 400, "message": "Error updating one resource"})


# Delete route
@stocks.route('/<id>', methods=["DELETE"])
def delete_stock(id):
    try:
        query = models.Stock.delete().where(models.Stock.id == id)
        query.execute()
        return jsonify(data='Resource successfully deleted', status={"code": 200, "message": "Resource successfully deleted"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 400, "message": "Error deleting resource"})
