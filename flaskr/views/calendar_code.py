import calendar as pycal

from flask import Blueprint, render_template, request, flash, url_for, redirect
from flaskr.python_helpers.cal_helpers import get_todays_date, get_month, user_events
from flaskr.python_helpers.week_functions import get_current_date, get_formatted_week, on_previous, create_month
from flaskr.python_helpers.month_functions import create_date, format_month, format_iters
from flaskr.python_helpers.day_functions import day_move, get_current_day, resetDate
from ..dbfunc.cal_funcs import import_calendar

from . import authenticate
from ..python_helpers.file_handling import validate_csv, allowed_files

cal_blueprint = Blueprint("calendar", __name__, url_prefix='/calendar')
pycal.setfirstweekday(6)


@cal_blueprint.route('/month/', methods=['GET', 'POST'])
@authenticate.login_required
def month():
    cal, header, year, month = create_month()
    mth = pycal.month_name[month]
    if request.method == 'POST':
        if 'upload_schedule' in request.files:
            sched = request.files['upload_schedule']

            if allowed_files(sched) and validate_csv(sched):
                import_calendar(None, None, None)
            else:
                flash("Bro, this ain\'t a calendar")
                return redirect(url_for('calendar.month'))
    return render_template('calendar/month.html', year=year, month=mth, day=cal, header=header)


@cal_blueprint.route('/week/', methods=['GET', 'POST'])
@authenticate.login_required
def week():
    if request.method == 'POST':
        on_previous()

    week = get_formatted_week()
    day, month, year = get_current_date()
    events = user_events()
    return render_template('calendar/week.html',
                           cal=pycal,
                           month=month,
                           year=year,
                           week=week,
                           events=events)


@cal_blueprint.route('/day/', methods = ['GET','POST'])
@authenticate.login_required
def day():
    if request.method == 'POST':
        if request.form.get('friend') == 'friend':
            print('test')
        elif request.form.get('move') == 'prev':
            day_move('prev')
        else:
            day_move('next')

        day, month, year = get_current_day()
    else:
        day, month, year = get_todays_date()
        resetDate()
    events = user_events()
    return render_template('calendar/day.html',
                           cal=pycal,
                           day=day,
                           month=month,
                           year=year,
                           events=events)


@cal_blueprint.route('/year/')
@authenticate.login_required
def year():
    return render_template('calendar/year.html')
