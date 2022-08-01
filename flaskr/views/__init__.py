from flask import Blueprint, redirect, url_for

main_blueprint = Blueprint("main", __name__, static_folder="../static")


@main_blueprint.route('/')
def home():
    return redirect(url_for('calendar.month'))


def init_app(app):
    # index route
    app.register_blueprint(main_blueprint)

    from . import calendar_code, authenticate
    app.register_blueprint(calendar_code.cal_blueprint)
    app.register_blueprint(authenticate.login_blueprint)
