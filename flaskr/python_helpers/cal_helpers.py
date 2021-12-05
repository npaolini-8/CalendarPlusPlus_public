import  calendar as pycal

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from ..dbfunc import cal_funcs as cf
from flask import g, session
from pytz import timezone


pycal.setfirstweekday(6)
cal = pycal.Calendar(6)
today = datetime.today()
day = today.day
month = today.month
year = today.year


def get_todays_date() -> (int, int, int):
    """Returns current day, month and year"""
    return day, month, year


def get_month_days() -> list:
    """Returns a list of all the days in the month"""
    days = cal.itermonthdays(year, month)
    return [d for d in days]


def get_month_dates() -> list:
    """Returns a list of all the dates in the month in the format [(year, month, day, weekday),
    (year, month, day++, weekday++),(year, month, day++, weekday++)...]"""
    dates = cal.itermonthdays4(year,month)
    return [dt for dt in dates]


def get_month() -> list:
    """Returns current month as a list of a list of tuples with pairs representing [[(day, weekday),
    (day++, weekday++),(day++, weekday++)...],[(),(),()]...]"""
    return cal.monthdays2calendar(year, month)


def get_week() -> (list, int):
    """Returns current week as a list of tuples representing (day, weekday) and week #"""
    # gets current week by checking if today's date is in the list
    curr_week = [week for week in get_month() for date, weekday in week if day is date][0]
    week_index = get_month().index(curr_week)
    return curr_week, week_index


def user_events() -> list:
    """Returns 2D array list of events with values and index representation as shown here
        values:     0   1     2      3     4     5      6      7       8      9      10      11   12  13
        index_val: id st_yr st_mon st_dy st_hr st_min end_yr end_mon end_dy end_hr end_min desc loc recur
       Note: index is still numeric, i.e 0,1,2,3..."""

    events = cf.get_event_list(session['user_id'], timezone('US/Eastern'))
    return events