from flask import Blueprint, render_template
from werkzeug.security import check_password_hash, generate_password_hash

login_blueprint = Blueprint("authenticate", __name__, url_prefix='/account')

@login_blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    return render_template('account/register.html')


@login_blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    return render_template('account/login.html')