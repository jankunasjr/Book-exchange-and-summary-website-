from flask import  Blueprint, flash, redirect, render_template, request, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from website.models import db, Users
from flask_login import login_user, login_required, logout_user, current_user, LoginManager

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template("login.html", boolean=True )

@auth.route('/logout')
def logout():
    return"<p>logout</p>"

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        Username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = Users.query.filter_by(Email=email).first()

        new_user = Users(Email=email, Username=Username, PasswordHash=password1,  RegistrationDate=datetime.utcnow(), UserRole = "Regular")

        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)
        flash('Account created!', category='success')
        return render_template("sign-up.html")

    return render_template("sign-up.html")
