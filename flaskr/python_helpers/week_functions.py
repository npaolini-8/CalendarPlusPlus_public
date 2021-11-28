from datetime import datetime, timedelta


# generate a list of hours (24-hr format)
def get_hours():
    start = datetime.today()
    stop = start + timedelta(hours=24)
    hours = []

    while start < stop:
        hour = 24 if start.hour == 0 else start.hour
        hours.append(f"{hour}:00")
        start += timedelta(hours=1)

    return hours
