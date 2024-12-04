from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from .extensions import db
from .models import Users, Inventory, Prompts, Transactions
from .auth import custom_generate_password_hash
import csv
from io import StringIO

profile = Blueprint('profile', __name__)


@profile.route('/', methods=['GET', 'POST'])
@login_required
def show_profile():
    # Fetch the current logged-in user's profile
    user = Users.query.get(current_user.UserID)

    if not user:
        flash('User not found.', category='error')
        return redirect(url_for('index'))  # Redirect to a safe default page

    if request.method == 'POST':
        # Update user details
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Input validation
        if not username or not email:
            flash('Username and email are required.', category='error')
            return redirect(url_for('profile.show_profile'))

        if password:
            # Hash the password using the custom hashing method
            user.PasswordHash = custom_generate_password_hash(password, method='pbkdf2:sha256')

        # Update the user's information
        user.Username = username
        user.Email = email

        try:
            db.session.commit()
            flash('Profile updated successfully!', category='success')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating your profile.', category='error')
            print(f"Error: {e}")

        return redirect(url_for('profile.show_profile'))

    return render_template("profile.html", user=user)

@profile.route('/download_csv/<table>', methods=['GET'])
@login_required
def download_csv(table):
    user_id = current_user.UserID
    output = StringIO()
    writer = csv.writer(output)

    if table == 'users':
        # Fetch user data
        user = Users.query.filter_by(UserID=user_id).first()
        if not user:
            flash("User not found.", "error")
            return redirect(url_for('profile.show_profile'))
        writer.writerow(['UserID', 'Username', 'Email', 'UserRole', 'RegistrationDate'])
        writer.writerow([user.UserID, user.Username, user.Email, user.UserRole.name, user.RegistrationDate])

    elif table == 'inventory':
        # Fetch inventory data
        items = Inventory.query.filter_by(OwnerID=user_id).all()
        writer.writerow(['BookID', 'Title', 'Author', 'Genre', 'Status', 'CreatedAt'])
        for item in items:
            writer.writerow([item.BookID, item.Title, item.Author, item.Genre, item.Status, item.CreatedAt])

    elif table == 'prompts':
        # Fetch prompts data
        prompts = Prompts.query.filter_by(UserID=user_id).all()
        writer.writerow(['PromptID', 'Name', 'SubmissionDate'])
        for prompt in prompts:
            writer.writerow([prompt.PromptID, prompt.Name, prompt.SubmissionDate])

    elif table == 'transactions':
        # Fetch transactions data
        transactions = Transactions.query.filter((Transactions.SenderID == user_id) | (Transactions.ReceiverID == user_id)).all()
        writer.writerow(['TransactionID', 'SenderID', 'ReceiverID', 'TransactionDate', 'Status'])
        for transaction in transactions:
            writer.writerow([transaction.TransactionID, transaction.SenderID, transaction.ReceiverID, transaction.TransactionDate, transaction.Status])

    else:
        flash("Invalid table selected.", "error")
        return redirect(url_for('profile.show_profile'))

    # Prepare the response
    output.seek(0)
    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = f"attachment; filename={table}_data.csv"
    response.headers["Content-Type"] = "text/csv"
    return response