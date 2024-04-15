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

@trades.route('/submit-trade', methods=['POST'])
def submit_trade():
    receiver_book_id = request.form.get('receiver_book_id')
    sender_book_id = request.form.get('sender_book_id')
    receiver = Inventory.query.get(sender_book_id)  # Get the receiver based on the sender's book
    if receiver:
        transaction = Transactions(ReceiverBookID=sender_book_id, SenderBookID=receiver_book_id, ReceiverID=receiver.OwnerID, SenderID=0, TransactionDate=datetime.now(), Status='Pending')
        db.session.add(transaction)
        db.session.commit()
        return redirect(url_for('trades.show_trades'))
    else:
        return "Book not found", 404
@trades.route('/trade-request/<int:book_id>')
def trade_request(book_id):
    book = Inventory.query.get(book_id)
    user_books = Inventory.query.filter_by(OwnerID=0).all()  # Fetch all books from the database owned by the user
    return render_template("trade_request.html", book=book, user_books=user_books)