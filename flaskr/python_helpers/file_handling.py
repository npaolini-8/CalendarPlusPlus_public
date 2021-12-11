ALLOWED_EXTENSIONS = {'ical', 'csv', 'ics'}


def allowed_files(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def validate_csv(csv):
    validate = True
    if '.' in csv and csv.rsplit('.', 1)[1].lower() == 'csv':
        # look for subject, start date, start time, end date, end time
        # description, location

        validate = False

    return validate


def get_extension(filename):
    return filename.rsplit('.', 1)[1].lower()


def export_wrapper():
    pass


def import_wrapper():
    pass
