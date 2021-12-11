import calendar as pycal
import os

from flask import Blueprint, render_template, request, flash, url_for, redirect, send_from_directory, abort, \
    current_app, session
from werkzeug.utils import secure_filename

from ..python_helpers.cal_helpers import get_todays_date, save_event, user_events, import_cal, export_cal, clear_path
from ..python_helpers.day_functions import day_move, get_current_day, resetDate
from ..python_helpers.week_functions import set_current_date, get_formatted_week, on_next, on_previous, reset_date
from ..python_helpers.month_functions import create_month, month_move, reset_month

from . import authenticate
from ..python_helpers.file_handling import allowed_files, get_extension

cal_blueprint = Blueprint("calendar", __name__, url_prefix='/calendar')
pycal.setfirstweekday(6)


def handle_import(doc_request, view):
    # save file object to variable
    sched = doc_request.files['upload_schedule']

    # validate if it can be used, reminder user else
    if allowed_files(sched.filename):

        # make the file secure and save the extension of file
        sched.filename = secure_filename(sched.filename)
        oldext = os.path.splitext(sched.filename)[1]
        file_path = os.path.join(current_app.config['TMP'], session['user_id'])

        # create file path if it doesn't exist and save the file so the database can pick it up
        if not os.path.exists(file_path) and not os.path.isdir(file_path):
            os.makedirs(file_path)
        sched.save(os.path.join(file_path, "import" + oldext))

        # import into database
        import_cal(get_extension(sched.filename))
    else:
        flash("Bro, this ain\'t a calendar we can use...", "info")

    return redirect(url_for('calendar.' + view))


def handle_export(extension):
    filename = 'export.' + extension
    export_cal(extension)

    # give it to user
    return send_from_directory(os.path.join(current_app.config['TMP'], session['user_id']), filename,
                               as_attachment=True)


@cal_blueprint.route('/month/', methods=['GET', 'POST'])
@authenticate.login_required
def month():
    if request.method == 'POST':

        # movement buttons
        if request.form.get('move') == "prev":
            month_move("prev")
        elif request.form.get('move') == "next":
            month_move("next")

        # try and give the server a schedule to use
        if request.form.get('upload') == "upload" and 'upload_schedule' in request.files:
            return handle_import(request, view="month")

        # check if form wants to export a file
        if request.form.get('export') == 'export' and request.form.get('exports'):
            extension = request.form.get('exports')
            return handle_export(extension)

    else:
        # reset all paths and start fresh if first time visiting page
        reset_month()
        clear_path()

    cal, header, year, month = create_month()
    events = user_events()

    return render_template('calendar/month.html', year=year, pycal=pycal, month=month, day=cal, header=header,
                           events=events)


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
            end_time = request.form.get('end-time')
            save_event(event_id, event_desc, start_date, end_date, start_time, end_time)

        # try and give the server a schedule to use
        if request.form.get('upload') == "upload" and 'upload_schedule' in request.files:
            return handle_import(request, view="week")

        # check if form wants to export a file
        if request.form.get('export') == 'export' and request.form.get('exports'):
            extension = request.form.get('exports')
            return handle_export(extension)

    else:
        reset_date()
        clear_path()

    day, month, year = set_current_date()
    week = get_formatted_week()
    events = user_events()
    return render_template('calendar/week.html',
                           cal=pycal,
                           month=month,
                           year=year,
                           week=week,
                           events=events)


@cal_blueprint.route('/day/', methods=['GET', 'POST'])
@authenticate.login_required
def day():
    if request.method == 'POST':

        print(request.form)
        if request.form.get('friend') == 'friend':
            print('test')
        elif request.form.get('move') == 'prev':
            day_move('prev')
        else:
            day_move('next')

        # try and give the server a schedule to use
        if request.form.get('upload') == "upload" and 'upload_schedule' in request.files:
            return handle_import(request, view="day")

        # check if form wants to export a file
        if request.form.get('export') == 'export' and request.form.get('exports'):
            extension = request.form.get('exports')
            return handle_export(extension)

        day, month, year = get_current_day()

    else:
        date, day, month, year = get_todays_date()
        resetDate()
        clear_path()

    events = user_events()
    return render_template('calendar/day.html',
                           cal=pycal,
                           day=day,
                           month=month,
                           year=year,
                           events=events)
