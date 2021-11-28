from flask import Blueprint, render_template
from . import authenticate
import calendar as pycal
from calendar import Calendar
from datetime import date, datetime, timedelta

cal_blueprint = Blueprint("calendar", __name__, url_prefix='/calendar')



