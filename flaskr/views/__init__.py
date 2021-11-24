from flask import Blueprint, render_template, redirect, url_for

main_blueprint = Blueprint("main", __name__, static_folder="../static")


@main_blueprint.route('/')
def home():
    return redirect(url_for('calendar.calendar'))
    #return render_template('calendar/yearly_view.html')



def init_app(app):
    # index route
    app.register_blueprint(main_blueprint)

    from . import calendar, authenticate
    app.register_blueprint(calendar.cal_blueprint)
    app.register_blueprint(authenticate.login_blueprint)


