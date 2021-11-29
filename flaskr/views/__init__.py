from flask import Blueprint, render_template, redirect, url_for

main_blueprint = Blueprint("main", __name__, static_folder="../static")


@main_blueprint.route('/')
def home():
<<<<<<< HEAD
    return redirect(url_for('calendar.month'))
=======
    return redirect(url_for('calendar.calendar'))
    #return render_template('calendar/yearly_view.html')
>>>>>>> fd2f2d2002f0ee4d78948a78bc9c2083a2b6493f



def init_app(app):
    # index route
    app.register_blueprint(main_blueprint)

    from . import calendar_code, authenticate
    app.register_blueprint(calendar_code.cal_blueprint)
    app.register_blueprint(authenticate.login_blueprint)


