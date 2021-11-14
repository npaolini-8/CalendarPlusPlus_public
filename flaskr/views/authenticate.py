from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.static import database_funcs as mongo


login_blueprint = Blueprint("authenticate", __name__, url_prefix='/account')


@login_blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        error = None

        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Password is required'

        mongo.CalDB().create_user(username, password, first_name, last_name)
        #if error is None:
        #flash(error)
    return render_template('account/register.html')


@login_blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method =='POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if user is None:
            error = 'Incorrect username'
        #elif not check_password_hash(user['password'], password):
            #error = 'Incorrect password'

        if error is None:
            session.clear()
            #session[]
            return redirect(url_for('index'))

        flash(error)

    return render_template('account/login.html')


@login_blueprint.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('index'))