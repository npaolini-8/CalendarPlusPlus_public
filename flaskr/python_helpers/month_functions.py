import calendar as pycal
import datetime as dt

def create_date():
    date = str(dt.date.today()).split("-")
    year = int(date[0])
    month = int(date[1])
    cal = pycal.TextCalendar(firstweekday=6).formatmonth(year, month).split("\n")
    cal.pop(0)
    return cal, year, month


def format_month(cal):
    for i in range(1, len(cal)):
        _str = list(cal[i])
        for j in range(len(_str)):
            if _str[j] == " ":
                if _str[j + 1] == " ":
                    _str[j + 1] = "0"
                    _str[j] = "0"
                    try:
                        if _str[j - 1] != " ":
                            _str[j] = " "
                            _str[j + 1] = " "
                    except IndexError:
                        pass

                elif int(_str[j + 1]) < 10:
                    try:
                        if _str[j + 2] == " ":
                            _str[j] = "0"
                    except IndexError:
                        pass

        cal[i] = "".join(_str)
        cal[i] = cal[i].split(" ")
    return cal


def format_iters(cal):
    # clean up residual formatting
    # and return lists iterable through jinja2
    cal[0] = cal[0].split(" ")
    header = cal.pop(0)
    for i in range(len(cal)):
        if cal[i][0] == "":
            cal[i][0] = 0

        cal[i] = [int(num) for num in cal[i] if num != ""]

    cal.pop()

    return cal, header
