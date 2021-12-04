import  calendar as pycal

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from ..dbfunc import cal_funcs as cf
from flask import g, session
from pytz import timezone


cal = pycal.Calendar(6)
today = datetime.today()
day = today.day
month = today.month
year = today.year


def get_date() -> tuple:
    """Returns current month and year"""
    return month, year


def get_hours() -> list:
    """Generates a list of hours (24-hr format)"""

    hours = []

    for hour in range(24):
        if hour < 10:
            hours.append(f"0{hour}:00")
        else:
            hours.append(f"{hour}:00")

    return hours


def get_week() -> list:
    """Returns the current week of the month as a list of tuples with the format (day_of_month, weekday)"""

    weeks = cal.monthdays2calendar(year, month)
    # gets current week by checking if today's date is in the list
    week = [week for week in weeks for date, weekday in week if day is date][0]
    week_index = weeks.index(week)
    week = format_week(week, week_index)

    return week


def format_week(week, index) -> list:
    """Replaces zeros with previous or upcoming days"""

    i = 0
    zeros = 0
    weekdays = []

    for day, weekday in week:
        if day == 0:
            zeros += 1

    # if zeros exist get the correct days for replacement
    if not zeros == 0:
        if index == len(cal.monthdayscalendar(year, month))-1:
            upcoming_month = (today + relativedelta(months=1)).month
            next_month = cal.monthdayscalendar(year, upcoming_month)
            next_week = next_month[0]
            start_index = len(next_week)-1-zeros
            other_days = next_week[start_index:len(next_week)]
        else:
            ending_month = (today - relativedelta(months=1)).month
            prev_month = cal.monthdayscalendar(year, ending_month)
            prev_week = prev_month[len(prev_month) - 1]
            other_days = prev_week[0:zeros]

    # replace 0 with correct day
    for day, weekday in week:
        if day == 0:
            weekdays.append(tuple([other_days[i], weekday]))
            i += 1
        else:
            weekdays.append(tuple([day, weekday]))

    return weekdays


def user_events():
    events = cf.get_event_list(session['user_id'], timezone('US/Eastern'))
    return events