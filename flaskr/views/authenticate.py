from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.static import database_funcs as mongo


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
    if request.method =='POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        user = db.find_user(username)

        if user is None:
            error = 'Incorrect username'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password'

        if error is None:
            session.clear()
            session['user_id'] = user['username']
            return redirect(url_for('main.home'))

        flash(error)

    return render_template('account/login.html')


@login_blueprint.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.home'))


@login_blueprint.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = db.find_user(user_id)


# def login_required(view):
#     @functools.wraps(view)
#     def wrapped_view(**kwargs):
#         if g.user is None:
#             return redirect(url_for('auth.login'))
#
#         return view(**kwargs)
#
#     return wrapped_view