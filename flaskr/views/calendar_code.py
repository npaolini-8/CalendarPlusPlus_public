import calendar as pycal
import datetime as dt

from flask import Blueprint, render_template
from flaskr.python_helpers.week_functions import get_hours
from flaskr.python_helpers.month_functions import create_date, format_month, format_iters
from flaskr.python_helpers.year_functions import create_jan, create_feb, create_march, create_april, create_may, create_july, create_june, create_august, create_september, create_october, create_november, create_december

from . import authenticate

cal_blueprint = Blueprint("calendar", __name__, url_prefix='/calendar')


@cal_blueprint.route('/month/')
@authenticate.login_required
def month():
    cal, year, month = create_date()
    cal = format_month(cal)
    cal, header = format_iters(cal)
    mth = pycal.month_name[month]
    return render_template('calendar/month.html', year=year, month=mth, day=cal, header=header)


@cal_blueprint.route('/week/')
@authenticate.login_required
def week():
    cal = pycal.Calendar()
    today = dt.date.today()
    day = today.day
    month = today.month
    year = today.year
    hours = get_hours()
    weeks = cal.monthdays2calendar(year, month)
    week = [week for week in weeks for date in week if day in date]
    week = week[0]
    return render_template('calendar/week.html', cal=pycal, month=month, year=year, hours=hours, week=week)


@cal_blueprint.route('/day/')
@authenticate.login_required
def day():
    return render_template('calendar/day.html')


@cal_blueprint.route('/year/')
@authenticate.login_required
def year():
    cal, year, jan = create_jan()
    cal, year, feb = create_feb()
    cal, year, mar = create_march()
    cal, year, apr = create_april()
    cal, year, may = create_may()
    cal, year, jun = create_june()
    cal, year, jul = create_july()
    cal, year, aug = create_august()
    cal, year, sep = create_september()
    cal, year, oct = create_october()
    cal, year, nov = create_november()
    cal, year, dec = create_december()
    cal = format_month(cal)
    cal, header = format_iters(cal)
    mth1 = pycal.month_name[jan]
    mth2 = pycal.month_name[feb]
    mth3 = pycal.month_name[mar]
    mth4 = pycal.month_name[apr]
    mth5 = pycal.month_name[may]
    mth6 = pycal.month_name[jun]
    mth7 = pycal.month_name[jul]
    mth8 = pycal.month_name[aug]
    mth9 = pycal.month_name[sep]
    mth10 = pycal.month_name[oct]
    mth11 = pycal.month_name[nov]
    mth12 = pycal.month_name[dec]
    return render_template('calendar/year.html', year=year, month1=mth1, month2=mth2, month3=mth3, month4=mth4, month5=mth5, month6=mth6, month7=mth7, month8=mth8, month9=mth9, month10=mth10, month11=mth11, month12=mth12, day=cal, header=header)
