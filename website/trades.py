from flask import Blueprint, render_template, request, redirect, url_for
from .models import Inventory, Users, Transactions
from sqlalchemy import join
from . import db
from datetime import datetime

trades = Blueprint('trades', __name__)

@trades.route('/show-trades')
def show_trades():
    current_user_id = 0 # Get the user ID from the session
    books = db.session.query(Inventory, Users).join(Users, Inventory.OwnerID == Users.UserID).filter(
        Inventory.Status == True, Inventory.OwnerID != current_user_id).all()
    return render_template("trades.html")