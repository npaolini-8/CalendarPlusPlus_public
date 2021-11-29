ALLOWED_EXTENSIONS = {'ical', 'csv', 'ics'}


def allowed_files(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


