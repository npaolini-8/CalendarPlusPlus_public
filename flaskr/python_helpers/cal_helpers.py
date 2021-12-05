import  calendar as pycal

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from ..dbfunc import cal_funcs as cf
from flask import g, session
from pytz import timezone

pycal.setfirstweekday(6)
cal = pycal
today = datetime.today()
day = today.day
month = today.month
year = today.year


def get_date():
    """Returns current month and year"""
    return day, month, year


def get_month_days():
    return [dates for dates in cal.itermonthdays(year, month)]


def get_month():
    """Returns current month as a list of dictionaries with key:value pairs representing weekday:day"""

    mth_cal = cal.monthcalendar(year, month)
    mth = []

    # convert month to a list of dictionaries with weekday as keys and day as value
    # i.e {6:12, 0:13, 1:14 ...} represents {Sunday:12th, Monday:13th, Tuesday:14th}
    for wk in mth_cal:
        dict = {}
        for index, wkday in enumerate(wk):
            # if the weekday is the first day of the week make key = 6 (represents Sunday)
            if index == 0:
                dict[6] = wkday
            else:
                dict[index-1] = wkday
        mth.append(dict)

    return mth


def user_events() -> list:
    """Returns 2D array list of events with values and index representation as shown here
        values:     0   1     2      3     4     5      6      7       8      9      10      11   12  13
        index_val: id st_yr st_mon st_dy st_hr st_min end_yr end_mon end_dy end_hr end_min desc loc recur
       Note: index is still numeric, i.e 0,1,2,3..."""

    events = cf.get_event_list(session['user_id'], timezone('US/Eastern'))
    return events