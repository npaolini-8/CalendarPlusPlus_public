import  calendar as pycal

from datetime import datetime
from dateutil.relativedelta import relativedelta as rd


cal = pycal.Calendar(6)
current_date = datetime.today()
day = current_date.day
month = current_date.month
year = current_date.year

def get_current_day():
    return day, month, year

def resetDate():
    global current_date
    global day
    global month
    global year
    current_date = datetime.today()
    day = current_date.day
    month = current_date.month
    year = current_date.year

def move(direction):
    global current_date
    global day
    global month
    global year
    if direction == 'prev':
        current_date = current_date - rd(days=1)
    else:
        current_date = current_date + rd(days=1)
    
    day = current_date.day
    month = current_date.month
    year = current_date.year
