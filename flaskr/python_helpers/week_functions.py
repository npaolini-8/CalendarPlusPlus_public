import  calendar as pycal

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from flaskr.python_helpers import cal_helpers as chs


cal = pycal.Calendar(6)
current_date = datetime.today()
day = current_date.day
month = current_date.month
year = current_date.year
week, index = chs.get_week()


def set_current_date(d=day, m=month, y=year) -> (int, int, int):
    """Returns current day, month, year shown on the selected week of the calendar"""
    return day, month, year


def get_formatted_week() -> list:
    """Returns the current week of the month as a list of tuples with the format (day_of_month, weekday)"""
    zeros = 0

    for day, weekday in week:
        if day == 0:
            zeros += 1

    # Replaces zeros with previous or upcoming days
    # if zeros exist get the correct days for replacement
    if zeros != 0:
        # if week is the last week in the month
        if index == 0:
            ending_month = (current_date - relativedelta(weeks=1)).month
            prev_month = cal.monthdayscalendar(month, ending_month)
            prev_week = prev_month[len(prev_month) - 1]
            other_days = prev_week[0:zeros]
        else:
            upcoming_month = (current_date + relativedelta(weeks=1)).month
            next_month = cal.monthdayscalendar(year, upcoming_month)
            next_week = next_month[0]
            start_index = len(next_week) - zeros
            other_days = next_week[start_index:len(next_week)]

    # replace 0 with correct day
    i = 0
    weekdays = []
    for day, weekday in week:
        if day == 0:
            weekdays.append(tuple([other_days[i], weekday]))
            i += 1
        else:
            weekdays.append(tuple([day, weekday]))

    return weekdays


def on_previous():
    """Updates month, day, year, week"""
    global index
    global week
    global month
    global year
    global day
    global current_date

    index = index - 1

    current_month = month
    current_date = datetime(year, month, day)
    current_date = current_date + relativedelta(weeks=-1)
    day = current_date.day
    year = current_date.year


    # if previous week is the end of the previous month
    if index < 0:
        month = current_date.month
        prev_cal_month = chs.get_month(year, month)
        index = len(prev_cal_month)-1
        week = prev_cal_month[index]
    else:
        if (index == 0 and current_date.month != current_month):
            month = current_date.month
            index = len(chs.get_month(year, month))-1

        week = chs.get_month(year, month)[index]