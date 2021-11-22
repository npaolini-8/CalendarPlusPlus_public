from flask import Blueprint, render_template, request
from . import authenticate
import calendar

cal_blueprint = Blueprint("calendar", __name__, url_prefix='/calendar')


@cal_blueprint.route('/my_calendar/')
@authenticate.login_required
def calendar():
    return render_template('calendar/calendar.html')


#@cal_blueprint.route('/year', methods=['GET', 'POST'])
#def yearly_view():
#    if request.method == 'POST':
#        print(calendar.calendar(2021))
#    else:
#        return render_template('calendar/calendar.html')