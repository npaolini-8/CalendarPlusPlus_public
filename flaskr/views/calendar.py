from flask import Blueprint, render_template, request
from . import authenticate


cal_blueprint = Blueprint("calendar", __name__, url_prefix='/calendar')


@cal_blueprint.route('/my_calendar/')
@authenticate.login_required
def calendar():
    return render_template('calendar/calendar.html')


@cal_blueprint.route('/yearView')
@authenticate.login_required
def yearly_view():
    return render_template('calendar/yearly_view.html')