import calendar as pycal
import datetime as dt


def create_month():
    date = dt.date.today()
    year = date.year
    month = date.month

    header = [day for day in pycal.day_abbr]
    header.insert(0, header.pop())

    # create the calendar
    cal = pycal.Calendar(6).monthdayscalendar(year, month)

    return cal, header, year, month
