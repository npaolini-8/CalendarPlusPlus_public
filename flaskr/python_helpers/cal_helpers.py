import  calendar as pycal

from datetime import datetime
from ..dbfunc import cal_funcs as cf
from flask import g, session
from pytz import timezone


pycal.setfirstweekday(6)
cal = pycal.Calendar(6)
current_date = datetime.today()
curr_day = current_date.day
curr_month = current_date.month
curr_year = current_date.year


def get_todays_date():
    """Returns the today's day, month and year"""
    return current_date, curr_day, curr_month, curr_year


def get_month_days(year=curr_year, month=curr_month) -> list:
    """Returns a list of all the days in the month"""
    days = cal.itermonthdays(year, month)
    return [d for d in days]


def get_month_dates(year=curr_year, month=curr_month) -> list:
    """Returns a list of all the dates in the month in the format [(year, month, day, weekday),
    (year, month, day++, weekday++),(year, month, day++, weekday++)...]"""
    dates = cal.itermonthdays4(year, month)
    return [dt for dt in dates]


def get_month(year=curr_year, month=curr_month) -> list:
    """Returns specified or current month as a list of week tuples with pairs representing [[(day, weekday),
    (day++, weekday++),(day++, weekday++)...],[(),(),()]...]"""
    return cal.monthdays2calendar(year, month)


def get_week(day=curr_day, year=curr_year, month=curr_month) -> (list, int):
    """Returns current week as a list of tuples representing (day, weekday) and week number"""
    # gets current week by checking if today's day is in the list
    weeks = get_month(year, month)
    curr_week = [week for week in weeks for date, weekday in week if day is date][0]
    week_index = get_month().index(curr_week)
    return curr_week, week_index


def user_events() -> list:
    """Returns 2D array list of events with values and index representation as shown here
        values:     0   1     2      3     4     5      6      7       8      9      10      11   12  13
        index_val: id st_yr st_mon st_dy st_hr st_min end_yr end_mon end_dy end_hr end_min desc loc recur
       Note: index is still numeric, i.e 0,1,2,3..."""
    events = cf.get_event_list(session['user_id'], timezone('US/Eastern'))
    return events


def save_event(event, desc, s_date, e_date, s_time, e_time):
    """Saves event to database"""
    # parse date and time
    s_date = s_date.split('-')
    e_date = e_date.split('-')
    s_time = s_time.split(':')
    e_time = e_time.split(':')

    # convert start and end time to database format
    start_time = cf.convert_date_input( s_date[0], s_date[1], s_date[2], s_time[0], s_time[0])
    end_time = cf.convert_date_input(e_date[0], e_date[1], e_date[2], e_time[0], e_time[0])

    cf.create_event(session['user_id'], event, start_time, end_time, desc)


#
# def edit_event():

