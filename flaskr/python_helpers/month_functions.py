import calendar as pycal
import datetime as dt
from dateutil.relativedelta import relativedelta as rd

from .cal_helpers import user_events

current_date = dt.date.today()
month = current_date.month
year = current_date.year


def create_month():
    header = [day for day in pycal.day_abbr]
    header.insert(0, header.pop())

    # create the calendar
    cal = pycal.Calendar(6).monthdayscalendar(year, month)

    return cal, header, year, month


def current_month():
    return month, year


def reset_month():
    global current_date
    global month
    global year

    current_date = dt.date.today()
    month = current_date.month
    year = current_date.year


def month_move(state):
    global current_date
    global month
    global year

    if state == 'prev':
        current_date = current_date - rd(months=1)
    elif state == 'next':
        current_date = current_date + rd(months=1)
    else:
        pass

    month = current_date.month
    year = current_date.year


def month_events():
    user_events()
