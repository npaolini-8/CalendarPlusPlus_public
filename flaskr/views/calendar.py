from flask import Blueprint, render_template
from . import authenticate

cal_blueprint = Blueprint("calendar", __name__, url_prefix='/calendar')


@cal_blueprint.route('/my_calendar/')
@authenticate.login_required
def calendar():
    return render_template('calendar/calendar.html')

