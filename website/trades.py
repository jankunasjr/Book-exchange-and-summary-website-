from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Inventory, Users, Transactions
from sqlalchemy import join
from . import db
from datetime import datetime

trades = Blueprint('trades', __name__)


@trades.route('/show-trades')
def show_trades():
    current_user_id = 2  # Get the user ID from the session
    books = db.session.query(Inventory, Users).join(Users, Inventory.OwnerID == Users.UserID).filter(
        Inventory.Status == True, Inventory.OwnerID != current_user_id).all()
    incoming_trades = db.session.query(Transactions, Inventory.Title, Users.Username).join(Inventory,
                                                                                           Transactions.SenderBookID == Inventory.BookID).join(
        Users, Transactions.SenderID == Users.UserID).filter(Transactions.ReceiverID == current_user_id,
                                                             Transactions.Status == 'Pending').all()

    return render_template("trades.html", books=books, incoming_trades=incoming_trades)


"""@trades.route('/submit-trade', methods=['POST'])
def submit_trade():
    receiver_book_id = request.form.get('receiver_book_id')
    sender_book_id = request.form.get('sender_book_id')
    sender_id = request.form.get('sender_id')

    if sender_id is not None:
        sender = Users.query.get(sender_id)  # Get the sender based on the sender_id
    else:
        return "Sender ID is missing", 400

    receiver = Inventory.query.get(receiver_book_id)  # Get the receiver based on the receiver's book

    if receiver is None or sender is None:
        return "Book or User not found", 404
    else:
        # Check if the receiver_book_id exists in the Inventory table
        receiver_book = Inventory.query.get(receiver_book_id)
        if receiver_book is None:
            return "Receiver book not found", 404
        else:
            transaction = Transactions(ReceiverBookID=receiver_book_id, SenderBookID=sender_book_id,
                                       ReceiverID=receiver.OwnerID, SenderID=sender_id, TransactionDate=datetime.now(),
                                       Status='Pending')
            db.session.add(transaction)
            db.session.commit()
            return redirect(url_for('trades.show_trades'))"""

@trades.route('/submit-trade', methods=['POST'])
def submit_trade():
    receiver_book_id = request.form.get('receiver_book_id')
    sender_book_id = request.form.get('sender_book_id')
    receiver = Inventory.query.get(sender_book_id)  # Get the receiver based on the sender's book
    if receiver:
        transaction = Transactions(ReceiverBookID=sender_book_id, SenderBookID=receiver_book_id, ReceiverID=receiver.OwnerID, SenderID=1, TransactionDate=datetime.now(), Status='Pending')
        db.session.add(transaction)
        db.session.commit()
        flash('Trade request has been sent successfully!', 'success')
        return redirect(url_for('trades.show_trades'))
    else:
        return "Book not found", 404

@trades.route('/trade-request/<int:book_id>')
def trade_request(book_id):
    book = Inventory.query.get(book_id)
    user_books = Inventory.query.filter_by(OwnerID=1).all()  # Fetch all books from the database owned by the user
    return render_template("trade_request.html", book=book, user_books=user_books)


@trades.route('/respond-trade', methods=['POST'])
def respond_trade():
    trade_id = request.form.get('trade_id')
    response = request.form.get('response')
    trade = Transactions.query.get(trade_id)
    if trade:
        if response == 'Accepted':
            # Get the books involved in the trade
            sender_book = Inventory.query.get(trade.SenderBookID)
            receiver_book = Inventory.query.get(trade.ReceiverBookID)

            # Swap the owner IDs of the books
            sender_book.OwnerID, receiver_book.OwnerID = receiver_book.OwnerID, sender_book.OwnerID

            # Update the trade status
            trade.Status = 'Accepted'

            db.session.commit()
            flash('Trade request accepted!', 'success')
        elif response == 'Rejected':
            trade.Status = 'Rejected'
            db.session.commit()
            flash('Trade request rejected!', 'error')
        else:
            return "Invalid response", 400

        return redirect(url_for('trades.show_trades'))
    else:
        return "Trade not found", 404
