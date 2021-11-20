import calendar as pycal
import datetime as dt

from flask import Blueprint, render_template
from flaskr.python_helpers.week_functions import get_hours
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
    return render_template('calendar/month.html', year=year, month=mth, day=cal, header=header)


@cal_blueprint.route('/week/')
@authenticate.login_required
def week():
    cal = pycal.Calendar()
    today = dt.date.today()
    day = today.day
    month = today.month
    year = today.year
    hours = get_hours()
    weeks = cal.monthdays2calendar(year, month)
    week = [week for week in weeks for date in week if day in date]
    week = week[0]
    return render_template('calendar/week.html', cal=pycal, month=month, year=year, hours=hours, week=week)


@cal_blueprint.route('/day/')
@authenticate.login_required
def day():
    return render_template('calendar/day.html')


@cal_blueprint.route('/year/')
@authenticate.login_required
def year():
    return render_template('calendar/year.html')