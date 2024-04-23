from flask import Blueprint, render_template, redirect, flash
from .models import Inventory, Reviews
from . import db
from flask import request, redirect, url_for
from datetime import datetime
from sqlalchemy.sql import func

inventory = Blueprint('inventory', __name__)

@inventory.route('/show-inventory')
def show_inventory():
    user_id = 1  # Hardcoded user ID
    books = Inventory.query.filter_by(OwnerID=user_id).all()  # Fetch all books from the database owned by the user

    # Calculate the average rating for each book
    for book in books:
        avg_rating = db.session.query(func.avg(Reviews.Rating)).filter(Reviews.BookID == book.BookID).scalar()
        book.average_rating = round(avg_rating, 2) if avg_rating else None

    return render_template("inventory.html", inventory=books)

@inventory.route('/submit-review', methods=['POST'])
def submit_review():
    print("submit_review function called")
    rating = request.form.get('rating')
    book_title = request.form.get('bookTitle')
    review_text = request.form.get('reviewText')
    user_id = request.form.get('userID')

    if not rating:
        flash('No rating selected.', category='error')
        return redirect(url_for('inventory.show_inventory'))

    if not 1 <= int(rating) <= 5:
        flash('Rating has to be  between 1 and 5.', category='error')
        return "Invalid rating. Rating should be between 1 and 5.", 400

    book = Inventory.query.filter(Inventory.Title.ilike(book_title)).first()

    if book:
        review = Reviews(BookID=book.BookID, UserID=user_id, Rating=rating, ReviewText=review_text, ReviewDate=datetime.now())
        try:
            db.session.add(review)  # Add the new review to the session
            db.session.commit()  # Commit the changes
            print(f"Review for {book_title} added with rating {rating}")
            flash('Review submitted.', category='success')
            return redirect(url_for('inventory.show_inventory')), 200  # Return a success status code
        except Exception as e:
            print(f"Error occurred: {e}")
            db.session.rollback()  # Rollback the changes in case of error
            return redirect(url_for('inventory.show_inventory')), 500  # Return a server error status code

    return redirect(url_for('inventory.show_inventory')), 404  # Return a not found status code if the book does not exist
