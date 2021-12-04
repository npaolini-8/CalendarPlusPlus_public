import  calendar as pycal

from datetime import datetime, timedelta
from ..dbfunc import cal_funcs as cf
from flask import g, session
from pytz import timezone

cal = pycal.Calendar(6)
today = datetime.today()
day = today.day
month = today.month
year = today.year


def get_date():
    return month, year


# generate a list of hours (24-hr format)
def get_hours():
    start = today
    stop = start + timedelta(hours=24)
    hours = []
    hour = start.hour

    while start < stop and hour < 23:
        hour = start.hour
        if hour < 10:
            hours.append(f"0{hour}:00")
        else:
            hours.append(f"{hour}:00")
        start += timedelta(hours=1)

    return hours


def get_week():
    weeks = cal.monthdays2calendar(year, month)
    week = [week for week in weeks for date in week if day in date]
    week = format_week(week[0])

    return week


def format_week(week):
    i = 0
    zeros = 0
    weekdays = []

    for day, weekday in week:
        if day == 0:
            zeros += 1

    if not zeros == 0:
        prev_month = cal.monthdayscalendar(year, month - 1)
        prev_week = prev_month[len(prev_month) - 1]
        prev_days = prev_week[0:zeros]

    for day, weekday in week:
        if day == 0:
            weekdays.append(tuple([prev_days[i], weekday]))
            i += 1
        else:
            weekdays.append(tuple([day, weekday]))

    return weekdays


def user_events():
    events = cf.get_event_list(session['user_id'], timezone('US/Eastern'))
    return events