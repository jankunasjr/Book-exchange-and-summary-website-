"""import sys
sys.path.insert(0, '/Users/emiliskeras/Desktop/Uni darbai/pkp/website')"""

import pytest
from flask import url_for
from website import create_app, db
from website.models import Inventory, Users, Transactions
from unittest.mock import patch
from jinja2 import Template
from datetime import datetime

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SERVER_NAME'] = 'localhost:5000'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://emiliskeras:raktas123@localhost/test_database'
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_show_trades(client, app):
    with app.app_context():
        response = client.get(url_for('trades.show_trades'))
    assert response.status_code == 200

def test_submit_trade(client, app):
    with app.app_context():
        # Create the users
        user1 = Users(UserID=1, Username='user1', PasswordHash='password1')
        user2 = Users(UserID=2, Username='user2', PasswordHash='password2')
        user3 = Users(UserID=0, Username='user3', PasswordHash='password3')  # Add this line
        db.session.add(user1)
        db.session.add(user2)
        db.session.add(user3)  # Add this line
        db.session.commit()

        # Create the books
        book1 = Inventory(OwnerID=1, Title='Book1', Author='Author1', Genre='Genre1', Status=True)
        book2 = Inventory(OwnerID=2, Title='Book2', Author='Author2', Genre='Genre2', Status=True)
        db.session.add(book1)
        db.session.add(book2)
        db.session.commit()

        # Make the POST request
        response = client.post(url_for('trades.submit_trade'), data=dict(
            receiver_book_id=1,
            sender_book_id=2,
            sender_id=0  # Change this line
        ), follow_redirects=True)
    assert response.status_code == 200


def test_submit_trade_invalid_book_id(client, app):
    with app.app_context():
        # Send a POST request to the submit_trade route with an invalid book ID
        response = client.post(url_for('trades.submit_trade'), data=dict(
            receiver_book_id=999,  # Invalid book ID
            sender_book_id=1,
            sender_id=1
        ), follow_redirects=True)
    assert response.status_code == 404  # Expect a 404 Not Found status code

def test_submit_trade_invalid_user_id(client, app):
    with app.app_context():
        # Send a POST request to the submit_trade route with an invalid user ID
        response = client.post(url_for('trades.submit_trade'), data=dict(
            receiver_book_id=1,
            sender_book_id=1,
            sender_id=999  # Invalid user ID
        ), follow_redirects=True)
    assert response.status_code == 404  # Expect a 404 Not Found status code

def test_submit_trade_invalid_user_id(client, app):
    with app.app_context():
        # Send a POST request to the submit_trade route with an invalid user ID
        response = client.post(url_for('trades.submit_trade'), data=dict(
            receiver_book_id=1,
            sender_book_id=1,
            sender_id=999  # Invalid user ID
        ), follow_redirects=True)
    assert response.status_code == 404  # Expect a 404 Not Found status code


def test_submit_trade_no_data(client, app):
    with app.app_context():
        # Send a POST request to the submit_trade route without data
        response = client.post(url_for('trades.submit_trade'), follow_redirects=True)
    assert response.status_code == 404  # Expect a 404 Not Found status code


def test_respond_trade_invalid_response(client, app):
    with app.app_context():
        # Create a trade
        trade = Transactions(ReceiverBookID=1, SenderBookID=2, ReceiverID=1, SenderID=2, TransactionDate=datetime.now(), Status='Pending')
        db.session.add(trade)
        db.session.commit()

        # Send a POST request to the respond_trade route with an invalid response
        response = client.post(url_for('trades.respond_trade'), data=dict(
            trade_id=trade.TransactionID,  # Valid trade ID
            response='Invalid'  # Invalid response
        ), follow_redirects=True)
    assert response.status_code == 500  # Expect a 500 Internal Server Error status code
