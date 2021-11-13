from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

login_blueprint = Blueprint("authenticate", __name__, url_prefix='/account')

@login_blueprint.route('/register/', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Password is required'

        #if error is None:
        #flash(error)
    return render_template('account/register.html')


@login_blueprint.route('/login/', methods=('GET', 'POST'))
def login():
    if request.method =='POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = ''

        if user is None:
            eroor = 'Incorrect username'
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