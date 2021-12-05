import  calendar as pycal

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from flaskr.python_helpers import cal_helpers as chs


cal = pycal.Calendar(6)
today = datetime.today()
day = today.day
month = today.month
year = today.year
week, index = chs.get_week()


def get_formatted_week() -> list:
    """Returns the current week of the month as a list of tuples with the format (day_of_month, weekday)"""
    i = 0
    zeros = 0
    weekdays = []

    for day, weekday in week:
        if day == 0:
            zeros += 1

    # Replaces zeros with previous or upcoming days
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