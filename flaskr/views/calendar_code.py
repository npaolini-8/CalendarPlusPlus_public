import calendar as pycal
import os

from ..dbfunc.cal_funcs import get_friends, find_user, add_friend, timezone, compare, friend_check

from flask import Blueprint, render_template, request, flash, url_for, redirect, send_from_directory, \
    current_app, session
from werkzeug.utils import secure_filename

from ..python_helpers.cal_helpers import get_todays_date, save_event, user_events, import_cal, export_cal, clear_path, \
    edit_event
from ..python_helpers.day_functions import day_move, get_current_day, resetDate
from ..python_helpers.week_functions import set_current_date, get_formatted_week, week_move, reset_date
from ..python_helpers.month_functions import create_month, month_move, reset_month

from . import authenticate
from ..python_helpers.file_handling import allowed_files, get_extension

cal_blueprint = Blueprint("calendar", __name__, url_prefix='/calendar')
pycal.setfirstweekday(6)


def handle_import(doc_request, view):
    """
    Handles all imports and delivers it to the database.
    After imports it will redirect the page to the appropriate page.

    :param doc_request: Web request (check Flask request)
    :param view: page to redirect to after import
    :return: Flask redirect
    """
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
    """
    Allows for view to receive a download for exports

    :param extension: file extension (csv, ical, ics)
    :return:
    """
    filename = 'export.' + extension
    export_cal(extension)

    # give it to user
    return send_from_directory(os.path.join(current_app.config['TMP'], session['user_id']), filename,
                               as_attachment=True)


@cal_blueprint.route('/month/', methods=['GET', 'POST'])
@authenticate.login_required
def month():
    free_time_block = []
    if request.method == 'POST':

        if request.form.get('friend-add') == 'friend':
            friend = find_user(request.form['friend-name'])  # validate friend
            if friend is not None:
                add_friend(session['user_id'], request.form['friend-name'])
            else:
                flash("Invalid User!")

        if request.form.get('compare-friends'):  # Schedule comparison operation
            compare_list = request.form.getlist('friend-check')  # returns all checked boxes as a list
            compare_list.append(session['user_id'])
            date = request.form.get('compare-date')
            free_time_block = compare(compare_list, date, timezone('US/Eastern'))

        # handle changing months
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

    # information handling
    cal, header, year, month = create_month()
    events = user_events()
    friends_list = get_friends(session['user_id'])  # get user friends(some may not be mutual)
    valid_friends = []
    for friend in friends_list:
        if friend_check(friend['username'], session['user_id']) == True:
            # only include users with currently logged in user on their friends lists
            valid_friends.append(friend)

    return render_template('calendar/month.html',
                           year=year,
                           cal=pycal,
                           month=month,
                           mdays=cal,
                           header=header,
                           events=events,
                           friends=valid_friends,
                           free_time_block=free_time_block)


@cal_blueprint.route('/week/', methods=['GET', 'POST'])
@authenticate.login_required
def week():
    free_time_block = []
    if request.method == 'POST':

        # add friends
        if request.form.get('friend-add') == 'friend':
            friend = find_user(request.form['friend-name'])
            if friend is not None:
                add_friend(session['user_id'], request.form['friend-name'])
            else:
                flash("Invalid User!")

        if request.form.get('compare-friends'):  # Schedule comparison operation
            compare_list = request.form.getlist('friend-check')  # returns all checked boxes as a list
            compare_list.append(session['user_id'])
            date = request.form.get('compare-date')
            free_time_block = compare(compare_list, date, timezone('US/Eastern'))

        if request.form.get('move') == 'prev':
            week_move("prev")
        elif request.form.get('move') == 'next':
            week_move("next")

        if request.form.get('event-button'):
            event_operation(request.form)

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

    friends_list = get_friends(session['user_id'])  # get user friends(some may not be mutual)
    valid_friends = []
    for friend in friends_list:
        if friend_check(friend['username'], session['user_id']) == True:
            # only include users with currently logged in user on their friends lists
            valid_friends.append(friend)

    mdays, header = create_month()[0], create_month()[1]

    return render_template('calendar/week.html',
                           cal=pycal,
                           month=month,
                           year=year,
                           week=week,
                           events=events,
                           friends=valid_friends,
                           mdays=mdays,
                           header=header,
                           free_time_block=free_time_block)


@cal_blueprint.route('/day/', methods=['GET', 'POST'])
@authenticate.login_required
def day():
    free_time_block = []
    if request.method == 'POST':
        if request.form.get('friend-add') == 'friend':  # add friend operation
            friend = find_user(request.form['friend-name'])  # look for new friend in DB
            if friend is not None:  # true if friend exists in DB, can be added to user's friend list
                add_friend(session['user_id'], request.form['friend-name'])
            else:
                flash("Invalid User!")  # friend passed is not real

        if request.form.get('compare-friends'):  # Schedule comparison operation
            compare_list = request.form.getlist('friend-check')  # returns all checked boxes as a list
            compare_list.append(session['user_id'])
            date = request.form.get('compare-date')
            free_time_block = compare(compare_list, date, timezone('US/Eastern'))

            # now that we have the user list, do comparisons here

        if request.form.get('event-button'):
            event_operation(request.form)

        if request.form.get('move') == 'prev':  # move backwards operation
            day_move('prev')
        elif request.form.get('move') == 'next':  # move forwards operation
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

    events = user_events()  # populate events
    friends_list = get_friends(session['user_id'])  # get user friends(some may not be mutual)
    valid_friends = []
    for friend in friends_list:
        if friend_check(friend['username'], session['user_id']) == True:
            # only include users with currently logged in user on their friends lists
            valid_friends.append(friend)

    mdays, header = create_month()[0], create_month()[1]

    return render_template('calendar/day.html',
                           cal=pycal,
                           day=day,
                           month=month,
                           year=year,
                           events=events,
                           friends=valid_friends,
                           mdays=mdays,
                           header=header,
                           free_time_block=free_time_block)


def event_operation(form):
    """
    Edit or save a given event on form request

    :param form: Form from request to get information from events
    """
    # parse form
    event_id = form['event-title']
    event_desc = form['event-desc']
    start_date = form['start-date']
    end_date = form['end-date']
    start_time = form['start-time']
    end_time = form['end-time']
    location = form['event-location']
    recurrence_type = form['recurrence']
    recurrence_count = form['recurrence-count']
    print(request.form)
    old_title = form['old-title']
    old_start_time = form['old-start-time']
    old_end_time = form['old-end-time']
    old_start_date = form['old-start-date']
    old_end_date = form['old-end-date']

    if form['event-button'] == 'save':  # save-op
        save_event(event_id, event_desc, start_date, end_date, start_time, end_time, location, rec_type = recurrence_type, rec_count = recurrence_count)
    elif form['event-button'] == 'update':  # update
        edit_event(event_id=old_title, start_time=old_start_time, end_time=old_end_time, start_date=old_start_date,
                   end_date=old_end_date, new_id=event_id, new_start_time=start_time, new_end_time=end_time,
                   new_start_date=start_date, new_end_date=end_date, new_desc=event_desc, new_loc=location,
                   delete=False)
    else:  # delete
        edit_event(event_id=old_title, start_time=old_start_time, end_time=old_end_time, start_date=old_start_date,
                   end_date=old_end_date, delete=True)
