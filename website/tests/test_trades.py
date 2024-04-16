"""import sys
sys.path.insert(0, '/Users/emiliskeras/Desktop/Uni darbai/pkp/website')"""

import pytest
from flask import url_for
from website import create_app, db
from website.models import Inventory, Users, Transactions
from unittest.mock import patch
from jinja2 import Template
from datetime import datetime
from config import SQLALCHEMY_DATABASE_URI

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SERVER_NAME'] = 'localhost:5000'
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    with app.app_context():
        db.create_all()
    yield app

@pytest.fixture
def client(app):
    return app.test_client()



def test_show_trades(client, app):
    with app.app_context():
        response = client.get(url_for('trades.show_trades'))
    assert response.status_code == 200

def test_submit_trade(client, app):
    with app.app_context():
        # Fetch the users
        user1 = Users.query.get(1)
        user2 = Users.query.get(2)
        user3 = Users.query.get(3)

        # Check if the users exist
        assert user1 is not None, "User with UserID 1 does not exist"
        assert user2 is not None, "User with UserID 2 does not exist"
        assert user3 is not None, "User with UserID 3 does not exist"

        # Fetch the books
        book1 = Inventory.query.get(1)
        book2 = Inventory.query.get(2)

        # Make the POST request
        response = client.post(url_for('trades.submit_trade'), data=dict(
            receiver_book_id=book1.BookID,
            sender_book_id=book2.BookID,
            sender_id=user3.UserID
        ), follow_redirects=True)
    assert response.status_code == 200

"""def test_submit_trade_valid_data(client, app):
    with app.app_context():
        # Fetch the users
        user1 = Users.query.get(1)
        user2 = Users.query.get(2)
        user3 = Users.query.get(3)

        # Print the users
        print(f'User 1: {user1}')
        print(f'User 2: {user2}')
        print(f'User 3: {user3}')

        # Check if the users exist
        assert user1 is not None, "User with UserID 1 does not exist"
        assert user2 is not None, "User with UserID 2 does not exist"
        assert user3 is not None, "User with UserID 3 does not exist"

        # Fetch the books
        book1 = Inventory.query.get(1)
        book2 = Inventory.query.get(2)

        # Make the POST request
        response = client.post(url_for('trades.submit_trade'), data=dict(
            receiver_book_id=book1.BookID,
            sender_book_id=book2.BookID,
            sender_id=user3.UserID
        ), follow_redirects=True)

        # Check the status code of the response
        assert response.status_code == 200

        # Check the content of the response
        assert 'Trade submitted successfully' in response.data.decode()"""

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
    assert response.status_code == 404

def test_submit_trade_invalid_user_id(client, app):
    with app.app_context():
        # Send a POST request to the submit_trade route with an invalid user ID
        response = client.post(url_for('trades.submit_trade'), data=dict(
            receiver_book_id=1,
            sender_book_id=1,
            sender_id=999  # Invalid user ID
        ), follow_redirects=True)
    assert response.status_code == 404


def test_submit_trade_no_data(client, app):
    with app.app_context():
        # Send a POST request to the submit_trade route without data
        response = client.post(url_for('trades.submit_trade'), follow_redirects=True)
    assert response.status_code == 404


def test_respond_trade_invalid_response(client, app):
    with app.app_context():
        # Create a new transaction
        new_transaction = Transactions(
            ReceiverBookID=1,  # Replace with actual book ID
            SenderBookID=2,  # Replace with actual book ID
            ReceiverID=1,  # Replace with actual user ID
            SenderID=2,  # Replace with actual user ID
            TransactionDate=datetime.now(),
            Status='Pending'
        )
        db.session.add(new_transaction)
        db.session.commit()

        # Now make the POST request with the new_transaction's ID
        response = client.post(url_for('trades.respond_trade'), data=dict(
            trade_id=new_transaction.TransactionID,  # Valid trade ID
            response='Invalid'  # Invalid response
        ), follow_redirects=True)
    assert response.status_code == 400  # Expect a 400 Bad Request status code