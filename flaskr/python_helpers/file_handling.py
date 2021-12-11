from ..dbfunc.cal_funcs import import_calendar, export_calendar

ALLOWED_EXTENSIONS = {'ical', 'csv', 'ics'}


def allowed_files(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_extension(filename):
    return filename.rsplit('.', 1)[1].lower()

