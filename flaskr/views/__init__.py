from flask import Blueprint, render_template, url_for

main_blueprint = Blueprint("main", __name__, static_folder="../static")


@main_blueprint.route('/')
def home():
    return render_template('index.html')


def init_app(app):
    # index route
    app.register_blueprint(main_blueprint)

    from .calendar import cal_blueprint as calendar
    app.register_blueprint(calendar)

    from .login import login_blueprint as login
    app.register_blueprint(login)
