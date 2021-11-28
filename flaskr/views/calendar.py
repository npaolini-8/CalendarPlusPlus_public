from flask import Blueprint, render_template
from . import authenticate

cal_blueprint = Blueprint("calendar", __name__, url_prefix='/calendar')


@cal_blueprint.route('/day_view/')
@authenticate.login_required
def day():
    return render_template('calendar/day.html')

@cal_blueprint.route('/week_view/')
@authenticate.login_required
def week():
    return render_template('calendar/week.html')

@cal_blueprint.route('/month_view/')
@authenticate.login_required
def month():
    return render_template('calendar/month.html')

@cal_blueprint.route('/year_view/')
@authenticate.login_required
def year():
    return render_template('calendar/year.html')