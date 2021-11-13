from flask import Blueprint, render_template

login_blueprint = Blueprint("login", __name__, url_prefix='/account')

@login_blueprint.route('/my_account/', methods=['GET', 'POST'])
def login():
    return render_template('account/login.html')