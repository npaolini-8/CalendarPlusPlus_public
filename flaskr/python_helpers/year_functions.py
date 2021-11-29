import calendar as pycal
import datetime as dt

date = str(dt.date.today()).split("-")
year = int(date[0])

def create_jan():
    jan = int(1)
    cal = pycal.TextCalendar(firstweekday=6).formatmonth(year, jan).split("\n")
    cal.pop(0)
    return cal, year, jan

def create_feb():
    feb = int(2)
    cal = pycal.TextCalendar(firstweekday=6).formatmonth(year, feb).split("\n")
    cal.pop(0)
    return cal, year, feb

def create_march():
    mar = int(3)
    cal = pycal.TextCalendar(firstweekday=6).formatmonth(year, mar).split("\n")
    cal.pop(0)
    return cal, year, mar

def create_april():
    apr = int(4)
    cal = pycal.TextCalendar(firstweekday=6).formatmonth(year, apr).split("\n")
    cal.pop(0)
    return cal, year, apr

def create_may():
    may = int(5)
    cal = pycal.TextCalendar(firstweekday=6).formatmonth(year, may).split("\n")
    cal.pop(0)
    return cal, year, may

def create_june():
    jun = int(6)
    cal = pycal.TextCalendar(firstweekday=6).formatmonth(year, jun).split("\n")
    cal.pop(0)
    return cal, year, jun

def create_july():
    jul = int(7)
    cal = pycal.TextCalendar(firstweekday=6).formatmonth(year, jul).split("\n")
    cal.pop(0)
    return cal, year, jul

def create_august():
    aug = int(8)
    cal = pycal.TextCalendar(firstweekday=6).formatmonth(year, aug).split("\n")
    cal.pop(0)
    return cal, year, aug

def create_september():
    sep = int(9)
    cal = pycal.TextCalendar(firstweekday=6).formatmonth(year, sep).split("\n")
    cal.pop(0)
    return cal, year, sep

def create_october():
    oct = int(10)
    cal = pycal.TextCalendar(firstweekday=6).formatmonth(year, oct).split("\n")
    cal.pop(0)
    return cal, year, oct

def create_november():
    nov = int(11)
    cal = pycal.TextCalendar(firstweekday=6).formatmonth(year, nov).split("\n")
    cal.pop(0)
    return cal, year, nov

def create_december():
    dec = int(12)
    cal = pycal.TextCalendar(firstweekday=6).formatmonth(year, dec).split("\n")
    cal.pop(0)
    return cal, year, dec