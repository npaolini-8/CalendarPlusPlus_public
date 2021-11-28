from flask import Blueprint, render_template
from . import authenticate
import calendar as pycal
from calendar import Calendar
from datetime import date, datetime, timedelta

cal_blueprint = Blueprint("calendar", __name__, url_prefix='/calendar')


@cal_blueprint.route('/day_view/')
@authenticate.login_required
def day():
    return render_template('calendar/day.html')

@cal_blueprint.route('/week_view/')
@authenticate.login_required
def calendar():
    return render_template('calendar/month.html')

@cal_blueprint.route('/year_view/')
@authenticate.login_required
def year():
    return render_template('calendar/year.html')

@cal_blueprint.route('/week/')
@authenticate.login_required
def week():
    cal = Calendar()
    today = date.today()
    day = today.day
    month = today.month
    year = today.year
    hours = get_hours()
    weeks = cal.monthdays2calendar(year, month)
    week = [week for week in weeks for date in week if day in date]
    week = week[0]
    return render_template('calendar/week.html', cal=pycal, month=month, year=year, hours=hours, week=week)


# generate a list of hours (24-hr format)
def get_hours():
    start = datetime.today()
    stop = start + timedelta(hours=24)
    hours = []

    while start < stop:
        hour = 24 if start.hour == 0 else start.hour
        hours.append(f"{hour}:00")
        start += timedelta(hours=1)

    return hours