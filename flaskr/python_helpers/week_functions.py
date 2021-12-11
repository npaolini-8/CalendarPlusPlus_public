import  calendar as pycal

from datetime import datetime
from dateutil.relativedelta import relativedelta
from flaskr.python_helpers import cal_helpers as chs


cal = pycal.Calendar(6)
current_date = datetime.today()
day = current_date.day
month = current_date.month
year = current_date.year
week, index = chs.get_week()
forward = False


def set_current_date() -> (int, int, int):
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
        if index == 0 and forward == False:
            ending_date = current_date - relativedelta(weeks=1)
            ending_month = ending_date.month
            ending_year = ending_date.year
            prev_month = cal.monthdayscalendar(year, ending_month)
            prev_week = prev_month[len(prev_month) - 1]
            other_days = prev_week[0:zeros]
        else:
            print("else block")
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


def on_next():
    """Updates month, day, year, week if the next arrow is clicked on the weekly view"""
    global index
    global week
    global month
    global year
    global day
    global current_date

    print(index)
    index += 1

    month_length = len(chs.get_month(year, month))
    current_date = current_date + relativedelta(weeks=1)

    # if next week is the beginning of the next month
    if index >= month_length:
        index = 0
        forward = True
        month = current_date.month
        year = current_date.year
        next_cal_month = chs.get_month(year, month)
        week = next_cal_month[index]
    else:
        # if we are still in the same month but moving to the next month and weeks overlap
        if index == month_length-1 and current_date.month != month:
            week = chs.get_month(year, month)[index]
            month = current_date.month
            year = current_date.year
        else:
            day = current_date.day
            year = current_date.year
            month = current_date.month
            week = chs.get_month(year, month)[index]


    print("end_index: ", index)
    print(f"day: {day}, month: {month}, year: {year}")
    print("week: ", week)

def on_previous():
    """Updates month, day, year, week if the previous arrow is clicked on the weekly view"""
    global index
    global week
    global month
    global year
    global day
    global current_date
    global forward

    forward = False
    index -= 1

    current_month = month
    current_date = datetime(year, month, day)
    current_date = current_date - relativedelta(weeks=1)
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


def reset_date():
    """Returns current day, month, year shown on the selected week of the calendar"""
    # reset date if user logs out
    global current_date
    global day
    global month
    global year
    global week
    global index

    current_date, day, month, year = chs.get_todays_date()
    week, index = chs.get_week()
    print("from reset:", day, month, year, week, index)