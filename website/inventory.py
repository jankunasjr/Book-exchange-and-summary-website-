from flask import Blueprint, render_template, request, jsonify
from .models import Inventory  # Assuming you have a Book model in your models.py file
from . import db
inventory = Blueprint('inventory', __name__)

@inventory.route('/show-inventory')
def show_inventory():
    user_id = 0  # Hardcoded user ID
    books = Inventory.query.filter_by(OwnerID=user_id).all()  # Fetch all books from the database owned by the user
    return render_template("inventory.html", inventory=books)
