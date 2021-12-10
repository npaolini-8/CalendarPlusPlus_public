import calendar as pycal

from flask import Blueprint, render_template, request, flash, url_for, redirect
from ..python_helpers.cal_helpers import get_todays_date, get_month, save_event, user_events
from ..python_helpers.day_functions import move, get_current_day, resetDate
from ..python_helpers.week_functions import set_current_date, get_formatted_week, on_next, on_previous
from ..python_helpers.month_functions import create_month
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
        if request.form.get('move') == 'prev':
            on_previous()
        elif request.form.get('move') == 'next':
            on_next()
        elif request.form.get('event-save') == 'save':
            event_id = request.form.get('event-title')
            event_desc = request.form.get('event-desc')
            start_date = request.form.get('start-date')
            end_date = request.form.get('end-date')
            start_time = request.form.get('start-time')
            end_time =request.form.get('end-time')
            save_event(event_id, event_desc, start_date, end_date, start_time, end_time)

    week = get_formatted_week()
    day, month, year = set_current_date()
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
        print(request.form)
        if request.form.get('friend') == 'friend':
            print('test')
        elif request.form.get('move') == 'prev':
            move('prev')
        else:
            move('next')

        date, day, month, year = get_current_day()
    else:
        date, day, month, year = get_todays_date()
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
