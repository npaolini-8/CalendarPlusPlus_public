from FLask import Blueprint, render_template

login_blueprint = Blueprint("login", __name__, url_prefix='login')

@login_blueprint.route('/my_account')
def login():
    return render_template('login.html')