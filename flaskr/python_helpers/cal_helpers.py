import calendar as pycal
import os
import shutil

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


def get_week(day=curr_day, year=curr_year, month=curr_month):
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


def save_event(event, desc, s_date, e_date, s_time, e_time, loc=None, rec_type=None, rec_count=None):
    """Saves event to database"""
    # parse date and time
    s_date = s_date.split('-')
    e_date = e_date.split('-')
    s_time = s_time.split(':')
    e_time = e_time.split(':')

    # convert start and end time to database format
    start_time = cf.convert_date_input(s_date[0], s_date[1], s_date[2], s_time[0], s_time[1], tz=timezone("US/Eastern"))
    end_time = cf.convert_date_input(e_date[0], e_date[1], e_date[2], e_time[0], e_time[1], tz=timezone("US/Eastern"))
    
    cf.create_event(session['user_id'], event, start_time, end_time, desc, loc, rec_type = rec_type, rec_count = rec_count)


def edit_event(event_id, start_time, end_time, start_date, end_date, new_id=None, new_start_time=None, new_end_time=None,
               new_start_date=None, new_end_date=None,new_desc=None, new_loc=None,
               delete=False):

    s_date = start_date.split('-')
    e_date = end_date.split('-')
    s_time = start_time.split(':')
    e_time = end_time.split(':')
    # convert start and end time to database format
    start = cf.convert_date_input(s_date[0], s_date[1], s_date[2], s_time[0], s_time[1], tz=timezone("US/Eastern"))
    end = cf.convert_date_input(e_date[0], e_date[1], e_date[2], e_time[0], e_time[1], tz=timezone("US/Eastern"))
    print(start)
    print(end)
    new_start = None
    new_end = None
    if not delete:
        ns_date = new_start_date.split('-')
        ne_date = new_end_date.split('-')
        ns_time = new_start_time.split(':')
        ne_time = new_end_time.split(':')

        new_start = cf.convert_date_input(ns_date[0], ns_date[1], ns_date[2], ns_time[0], ns_time[1], tz=timezone("US/Eastern"))
        new_end = cf.convert_date_input(ne_date[0], ne_date[1], ne_date[2], ne_time[0], ne_time[1], tz=timezone("US/Eastern"))

        print(new_start)
        print(new_end)
    """Edits event in database"""
    cf.edit_event(session['user_id'], event_id, start, end, new_id, new_start, new_end, new_desc,
                  new_loc, delete=delete)


tmp_path = "flaskr/static/tmp"


def export_cal(format, tz=None):
    file_path = os.path.join(tmp_path, session['user_id'])
    if not os.path.exists(file_path) and not os.path.isdir(file_path):
        os.makedirs(file_path)
    zone = tz if tz else timezone('US/Eastern')
    return cf.export_calendar(session['user_id'], format, zone)


def import_cal(format, tz=None):
    file_path = os.path.join(tmp_path, session['user_id'])
    if not os.path.exists(file_path) and not os.path.isdir(file_path):
        os.makedirs(file_path)
    zone = tz if tz else timezone('US/Eastern')
    return cf.import_calendar(session['user_id'], cal_str="???", format=format, tz=zone)


def clear_path():
    file_path = os.path.join(tmp_path, session['user_id'])
    if os.path.exists(file_path) and os.path.isdir(file_path):
        shutil.rmtree(file_path)
