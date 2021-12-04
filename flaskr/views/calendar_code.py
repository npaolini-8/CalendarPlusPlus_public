import calendar as pycal

from flask import Blueprint, render_template
from flaskr.python_helpers.week_functions import get_hours, get_week, get_date, user_events
from flaskr.python_helpers.month_functions import create_date, format_month, format_iters

from . import authenticate

cal_blueprint = Blueprint("calendar", __name__, url_prefix='/calendar')


@cal_blueprint.route('/month/')
@authenticate.login_required
def month():
    cal, year, month = create_date()
    cal = format_month(cal)
    cal, header = format_iters(cal)
    mth = pycal.month_name[month]
    return render_template('calendar/month.html',
                           year=year,
                           month=mth,
                           day=cal,
                           header=header)


@cal_blueprint.route('/week/')
@authenticate.login_required
def week():
    cal = pycal.Calendar()
    month, year = get_date()
    hours = get_hours()
    week = get_week()
    events = user_events()
    return render_template('calendar/week.html',
                           cal=pycal,
                           month=month,
                           year=year,
                           hours=hours,
                           week=week,
                           events=events)


@cal_blueprint.route('/day/')
@authenticate.login_required
def day():
    return render_template('calendar/day.html')


@cal_blueprint.route('/year/')
@authenticate.login_required
def year():
    return render_template('calendar/year.html')
