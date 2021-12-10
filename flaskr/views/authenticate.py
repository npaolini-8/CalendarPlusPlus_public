from functools import wraps
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from flaskr.python_helpers.week_functions import reset_date
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.dbfunc import database_funcs as mongo

login_blueprint = Blueprint("auth", __name__, url_prefix='/account')
db = mongo.CalDB()


@login_blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        error = None

        user = db.find_user(username)

        if user is not None:
            error = f"User {username} is already registered. Try again"
            return redirect(url_for('auth.register'))

        if error is None:
            password = generate_password_hash(password)
            db.create_user(username, password, first_name, last_name)
            error = f"Welcome {username}! Thank you for registering."
            return redirect(url_for('main.home'))

        flash(error)
    return render_template('account/register.html')


@login_blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        user = db.find_user(username)

        if user is None or not check_password_hash(user['password'], password):
            error = 'Invalid credentials. Please try again.'
            flash(error)
            return redirect(url_for('auth.login'))

        if error is None:
            session.clear()
            session['user_id'] = user['username']
            return redirect(url_for('calendar.month'))
        flash(error)

    return render_template('account/login.html')


@login_blueprint.route('/logout/')
def logout():
    reset_date()
    session.clear()
    return redirect(url_for('auth.login'))


# registers a function that runs before the view, no matter what URL is requested
# code snippet taken from https://flask.palletsprojects.com/en/2.0.x/tutorial/views/
@login_blueprint.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = db.find_user(user_id)


# This decorator returns a new view function that wraps the original view it’s applied to.
# The new function checks if a user is loaded and redirects to the login page otherwise.
# If a user is loaded the original view is called and continues normally.
# code snippet taken from https://flask.palletsprojects.com/en/2.0.x/tutorial/views/
def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
