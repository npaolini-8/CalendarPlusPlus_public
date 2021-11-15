from flask import Blueprint, render_template


cal_blueprint = Blueprint("calendar", __name__, url_prefix='/calendar')


@cal_blueprint.route('/my_calendar/')
def calendar():
    return render_template('calendar/calendar.html')