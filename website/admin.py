from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from functools import wraps
from .models import UserRoleEnum, Users, Inventory, Prompts, Transactions, ChatMessages
from .extensions import db

admin = Blueprint('admin', __name__)


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.UserRole != UserRoleEnum.Admin:
            flash('You do not have access to this page.', 'error')
            return redirect(url_for('views.home'))  # Redirect to home or login page
        return f(*args, **kwargs)

    return decorated_function


@admin.route('/')
@login_required
@admin_required
def admin_dashboard():
    # Fetch data from all tables
    users = Users.query.all()
    inventory = Inventory.query.all()
    prompts = Prompts.query.all()
    transactions = Transactions.query.all()
    chat_messages = ChatMessages.query.all()

    return render_template(
        'admin_dashboard.html',
        users=users,
        inventory=inventory,
        prompts=prompts,
        transactions=transactions,
        chat_messages = chat_messages
    )


@admin.route('/update/<table>/<int:id>', methods=['POST'])
@login_required
@admin_required
def update_table(table, id):
    # Update a specific row in a given table
    try:
        if table == 'users':
            user = Users.query.get(id)
            user.Username = request.form.get('username')
            user.Email = request.form.get('email')
            db.session.commit()
        elif table == 'inventory':
            book = Inventory.query.get(id)
            book.Title = request.form.get('title')
            book.Author = request.form.get('author')
            book.Genre = request.form.get('genre')
            db.session.commit()
        elif table == 'prompts':
            prompt = Prompts.query.get(id)
            prompt.Name = request.form.get('name')
            db.session.commit()
        elif table == 'transactions':
            transaction = Transactions.query.get(id)
            transaction.Status = request.form.get('status')
            db.session.commit()
        elif table == 'chat_messages':
            message = ChatMessages.query.get(id)
            message.MessageText = request.form.get('message_text')
            db.session.commit()
        else:
            flash('Invalid table specified.', 'error')
            return redirect(url_for('admin.admin_dashboard'))

        flash(f'{table.capitalize()} record updated successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating record: {e}', 'error')

    return redirect(url_for('admin.admin_dashboard'))

@admin.route('/delete/<table>/<int:id>', methods=['POST'])
@login_required
@admin_required
def delete_record(table, id):
    try:
        if table == 'users':
            record = Users.query.get(id)
        elif table == 'inventory':
            record = Inventory.query.get(id)
        elif table == 'prompts':
            record = Prompts.query.get(id)
        elif table == 'transactions':
            record = Transactions.query.get(id)
        elif table == 'chat_messages':
            record = ChatMessages.query.get(id)
        else:
            flash('Invalid table specified.', 'error')
            return redirect(url_for('admin.admin_dashboard'))

        if not record:
            flash('Record not found.', 'error')
            return redirect(url_for('admin.admin_dashboard'))

        db.session.delete(record)
        db.session.commit()
        flash(f'{table.capitalize()} record deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting record: {e}', 'error')

    return redirect(url_for('admin.admin_dashboard'))