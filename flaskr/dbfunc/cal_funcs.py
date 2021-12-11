from os import write
from datetime import datetime, timedelta, tzinfo
from re import split  # Used to get timestamps for database information
from icalendar import Calendar, Event
import pytz
from pytz import timezone
import csv
from io import StringIO
from dateutil.relativedelta import relativedelta
import os
from .database_funcs import CalDB #TODO make sure . is here before push

calendar_db = CalDB()

tmp_path = "flaskr/static/tmp"

#TODO
#GENERAL: refactor log-in to not include password comparison
#import
#create function to test for ICS validity, name, start, end DONEish
#make sure import works for ics strings DONE
#make sure tz conversion works DONE
#function to check csv validity, google csv
#manage incoming strings as CSV
#export
#modify export return to formatted string DONE
#create csv template info DONE

#to be used for converting normal input into our datestring format, tz = pytz object of user timezone
#can take int or string input, but assumes they are all the same
#time switched to optional for more convenient input
def convert_date_input( year, month, day, hour=None, minute=None, tz=pytz.utc) -> str:

    if type(year) is str:
        year = int(year)
        month = int(month)
        day = int(day)
        if hour is not None:
            hour = int(hour)
        else:
            hour = 0
        if minute is not None:
            minute = int(minute)
        else:
            minute = 0

    dt = tz.localize(datetime(year, month, day, hour, minute))

    dt = dt.astimezone(pytz.utc)

    return dt.strftime("%Y%m%dT%H%M%SZ")


# returns in str: <x> days, hr:min:sec
def get_time_delta(start, end):
    # parse strings into datetime
    start = get_datetime(start)
    end = get_datetime(end)

    # extract date from datetime
    # NOTE:IF we want PURELY date output can do this
    # start = start.date()
    # end = end.date()

    return end - start


# start and end params to get events in a given date range, after a start date, or before an end date
# they are assumed to be string input in out db form, can use above convert_date_input for conversion
# tz is the users chosen timezone, function converts to this timezone before returning
# tz of the form timezone('US/Eastern'), you can print(pytz.common_timezones_set) to see the tzs
# NOTE: START AND END ARE EXPECTED TO BE IN UTC, use convert_date_input if need be
def get_event_list(username, tz, start=None, end=None, ) -> list:
    # return list of dicts, converting to 2D list
    # 0  1     2      3     4     5      6      7       8      9      10      11   12  13
    # id st_yr st_mon st_dy st_hr st_min end_yr end_mon end_dy end_hr end_min desc loc recur

    # desc and loc might be None, recur is set to 0 for non-recurring events, non-zero for recurring
    # all recurring events will have the same recur value as the other events in their series
    events = calendar_db.get_event_list(username, start=None, end=None)

    req_events = []

    # two dates input, include all events BETWEEN them
    if start is not None and end is not None:
        start = get_datetime(start)
        end = get_datetime(end)

        for event in events:
            s_date = get_datetime(event["start_time"])
            e_date = get_datetime(event["end_time"])

            if e_date >= start and s_date <= end:
                req_events.append(event)
    elif start is not None:  # only start given, include all events AFTER
        start = get_datetime(start)

        for event in events:
            s_date = get_datetime(event["start_time"])

            if start <= s_date:
                req_events.append(event)

    elif end is not None:  # only end given, include all events BEFORE
        end = get_datetime(end)

        for event in events:
            s_date = get_datetime(event["start_time"])

            if s_date <= end:
                req_events.append(event)
    else:
        req_events = events

    return_list = []

    for event in req_events:
        row = []
        row.append(event["event_id"])

        date = get_datetime(event["start_time"])
        date = date.astimezone(tz)

        # duplicated code come get me
        date_comps = get_date_components(date.strftime("%Y%m%dT%H%M%SZ"))
        for comp in date_comps:
            row.append(int(comp))
        # row.append(event["start_time"])

        date = get_datetime(event["end_time"])
        date = date.astimezone(tz)

        date_comps = get_date_components(date.strftime("%Y%m%dT%H%M%SZ"))
        for comp in date_comps:
            row.append(int(comp))

        # row.append(event["end_time"])
        row.append(event["description"])
        row.append(event["location"])
        row.append(event["recurrence"])
        return_list.append(row)

    return return_list


#builds calendar file based on given format: ics, csv
def export_calendar( username, format, tz):

    good_input = True

    #db queries
    try:
        user = calendar_db.find_user(username)
        events = user["events"]

        if format.lower() == "ics":
            #generate icalendar object from db events
            #TODO: do we want to pass username and build that into ical file description?
            cal = build_ics( events, tz )
            #generates byte string from ical object
            data = cal.to_ical()
            #print(data)

            #converts byte string to string and returns (string version)
            #output_str = data.decode("utf-8")
            #print(output_str.strip())
            #return data.decode("utf-8")

            #writes file
            with open( os.path.join(tmp_path, username, "export.ics"), 'wb') as ical_file:
                ical_file.write(data)


        elif format.lower() == "csv" :
            csv_cal = build_csv( events, tz )

            with open( os.path.join(tmp_path, username, "export.csv"), 'w', encoding='utf-8') as csv_handler:
                #instead of file write to string io
                #csv_handler = StringIO()
                writer = csv.writer(csv_handler)

                for row in csv_cal:
                    #print(row)
                    writer.writerow(row)
                csv_handler.close()

                #string version
                #move iterator back to start of file and print
                #csv_handler.seek(0)
                #return csv_handler.read().strip()
                #csv_handler.seek(0)
                #print(csv_handler.read().strip()) #NOTE THIS WILL NOT WORK IF RETURN IS INCLUDED W/O ANOTHER SEEK
    except Exception as e:
        print(e)
        good_input = False

    return good_input


def build_ics( events, tz ) -> Calendar:

    cal = Calendar()
    id = 0

    # required header for compatibility
    cal.add('version', '2.0')
    cal.add('prodid', '-//calendarplusplus export//')  # can put anything here wrapped in the slashes i think...

    # icals are populated by event subcomponents, loop builds event subcomponents from DB and adds them to calendar
    for item in events:
        event = Event()

        # event.add( 'uid', str(id))
        id += 1

        date = get_datetime(item["start_time"])
        date = date.astimezone(tz)
        event.add('dtstart', date)

        date = get_datetime(item["end_time"])
        date = date.astimezone(tz)
        event.add('dtend', date)

        # adds datestamp for format compliance
        # TODO: do we want to save datestemp (when event was added) in our db?
        event.add('dtstamp', datetime.now(pytz.utc))

        event.add('summary', item["event_id"])

        # accounting for optional fields
        if item["description"] is not None:
            event.add('description', item["description"])

        if item["location"] is not None:
            event.add('location', item["location"])

        cal.add_component(event)

    return cal


# returns datetime object built from datetime string from db
# format: YYYYMMDDTHHMMSS
# assumes we are storing in utc, tags objects accordingly
def get_datetime(datestr) -> datetime:
    # year = int(datestr[0:4])
    # month = int(datestr[4:6])
    # day = int(datestr[6:8])

    # hour = int(datestr[9:11])
    # minute = int(datestr[11:13])

    datestr = datestr.replace('\xad', '')
    date_components = get_date_components(datestr)
    # print(date_components)

    # return datetime(year,month,day,hour,minute, tzinfo=pytz.utc)
    return datetime(int(date_components[0]), int(date_components[1]), int(date_components[2]), int(date_components[3]),
                    int(date_components[4]), tzinfo=pytz.utc)


def get_date_components(datestr):
    year = datestr[0:4]
    month = datestr[4:6]
    day = datestr[6:8]

    hour = datestr[9:11]
    minute = datestr[11:13]

    return [year, month, day, hour, minute]


def build_csv( events, tz):

    # csv_data : List[List[str]] = []
    csv_data = []

    # add header
    row = ["Subject", "Start Date", "Start Time", "End Date", "End Time", "Description", "Location"]
    csv_data.append(row)

    for item in events:

        #TODO: Timezone in google csv? Are we going to get this from front end?
        start = get_datetime(item["start_time"])
        start = start.astimezone(tz)
        end = get_datetime(item["end_time"])
        end = end.astimezone(tz)

        start_components = get_date_components(start.strftime("%Y%m%dT%H%M%SZ"))
        end_components = get_date_components(end.strftime("%Y%m%dT%H%M%SZ"))

        start_date = start_components[1] + "/" + start_components[2] + "/" + start_components[0]
        start_time = start_components[3] + ":" + start_components[4]

        end_date = end_components[1] + "/" + end_components[2] + "/" + end_components[0]
        end_time = end_components[3] + ":" + end_components[4]

        row = [item["event_id"], start_date, start_time, end_date, end_time]

        # accounting for optional fields again
        if item["description"] is not None:
            row.append(item["description"])

        if item["location"] is not None:
            row.append(item["location"])

        csv_data.append(row)

    # print(csv_data)
    return csv_data



#TODO: add accounting for optional fields, done for ICS
#RETURNS BOOLEAN: True if no failures from input, False if Exceptions show up
#this is likely to catch all formatting failures as the type conversions rely on specific input

def import_calendar( username, cal_str, format, tz ):

    good_input = True

    #assuming string input from app this file read would simply stay as variable input
    #file read done for testing

    events = calendar_db.find_user(username)["events"]

    if format == "ics":
        try:
            cal = Calendar()
            cal_file = open(os.path.join(tmp_path, username, "import.ics"), 'r')
            cal_str = cal_file.read()
            components = cal.from_ical(cal_str)

            #strftime string is formatted string output from datetime object to match current convention
            #source: https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
            for component in components.walk():
                if component.name == "VEVENT":
                    #print(component.get('summary'))
                    # print(component.get('dtstart').dt.astimezone(pytz.utc).strftime("%Y%m%dT%H%M%SZ"))
                    # print(component.decoded('dtstart'))
                    # print(component.get('dtend').dt.astimezone(pytz.utc).strftime("%Y%m%dT%H%M%SZ"))

                    #start = tz.localize(component.get('dtstart').dt)
                    start = component.get('dtstart').dt
                    if start.tzinfo is None:
                        start = tz.localize(start)
                    start = start.astimezone(pytz.utc).strftime("%Y%m%dT%H%M%SZ")

                    #end = tz.localize(component.get('dtend').dt)
                    end = component.get('dtend').dt
                    if end.tzinfo is None:
                        end = tz.localize(end)
                    end = end.astimezone(pytz.utc).strftime("%Y%m%dT%H%M%SZ")

                    events.append({"event_id":component.get('summary'),"start_time":component.get('dtstart').dt.astimezone(pytz.utc).strftime("%Y%m%dT%H%M%SZ"),\
                        "end_time":component.get('dtend').dt.astimezone(pytz.utc).strftime("%Y%m%dT%H%M%SZ"), "description":component.get('description'),  "location":component.get('location'),
                                   "recurrence":0})
        except Exception:
            good_input = False


    # TODO: timezone again for google csv format, not sure if it is ever listed. we may need to "assume" based on selected timezone of current user
    # TODO: this works for expected format of subject, start date, start time, end date, end time, description, and location, need to test for other cases
    elif format == "csv":
        try:
            with open(os.path.join(tmp_path, username, "import.csv"), 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                #csv_reader = csv.DictReader(cal_str, delimiter=',')
                #csv_reader.fieldnames = ["Subject","Start Date","Start Time","End Date","End Time","Description","Location"]

                for row in csv_reader:
                    subj = row['Subject']

                    #I duplicated code here, i might fix eventually
                    csv_start_date = row['Start Date']

                    #finding /s to account for inconsistent format
                    s_start_date = csv_start_date.split('/')

                    #accounts for 2 digit year input
                    if len(s_start_date[2]) == 2:
                        s_start_date[2] = "20" + s_start_date[2]

                    csv_start_time = row['Start Time']

                    #splitting to account for AM/PM addition
                    s_start_time = csv_start_time.split()
                    start_time_digits = s_start_time[0].split(":")

                    #check for am/pm listing and modify hour accordingly
                    if len(s_start_time) > 1:
                        if s_start_time[1] == "AM":
                            if start_time_digits[0] == "12":
                                start_time_digits[0] = "00"
                        elif s_start_time[1] == "PM":
                            if start_time_digits[0] != "12":
                                start_time_digits[0] = str( int(start_time_digits[0]) + 12)

                    start_dt = datetime(int(s_start_date[2]),int(s_start_date[0]), int(s_start_date[1]),int(start_time_digits[0]),int(start_time_digits[1]))
                    start_dt = tz.localize(start_dt)
                    start_string = start_dt.astimezone(pytz.utc).strftime("%Y%m%dT%H%M%SZ")

                    csv_end_date = row['End Date']

                    s_end_date = csv_end_date.split('/')

                    #accounts for 2 digit year input
                    if len(s_end_date[2]) == 2:
                        s_end_date[2] = "20" + s_end_date[2]

                    csv_end_time = row['End Time']

                    #splitting to account for AM/PM addition
                    s_end_time = csv_end_time.split()
                    end_time_digits = s_end_time[0].split(":")

                    #check for am/pm listing and modify hour accordingly
                    if len(s_end_time) > 1:
                        if s_end_time[1] == "AM":
                            if end_time_digits[0] == "12":
                                end_time_digits[0] = "00"
                        elif s_end_time[1] == "PM":
                            if end_time_digits[0] != "12":
                                end_time_digits[0] = str( int(end_time_digits[0]) + 12)

                    end_dt = datetime(int(s_end_date[2]),int(s_end_date[0]), int(s_end_date[1]),int(end_time_digits[0]),int(end_time_digits[1]))
                    end_dt = tz.localize(end_dt)
                    end_string = end_dt.astimezone(pytz.utc).strftime("%Y%m%dT%H%M%SZ")

                    desc = row['Description']
                    loc = row['Location']

                    events.append({"event_id": subj,"start_time": start_string,"end_time": end_string,"description": desc, "location": loc, "recurrence": 0 })
        except Exception as e:
            print(e)
            good_input = False

    calendar_db.update_event_list(username,events)
    return good_input

#checks if f_username is on username's friend list
def friend_check(username, f_username):
    friends = calendar_db.get_friends(username)["friends"]
    for friend in friends:
        if friend["username"] == f_username:
            return True
    
    return False

#recurrence takes day, week, month, year
#rec_count is the number of times the event recurrs, EXCLUDING the first event
#start/end time expecting UTC datetime strings, use convert_date_input
#start/end are for the first event of the series
def create_rec_event( username, event_id, start_time, end_time, recurrence, rec_count, description=None, location=None):

    #events = calendar_db.find_user(username)["events"]
    events = []
    rec_count += 1 #adds the first event

    start_time = get_datetime(start_time)
    end_time = get_datetime(end_time)

    rec_id = calendar_db.get_rec_id(username)

    if recurrence == "day":
        for i in range(rec_count):
            #increment after to make sure we get initial day
            start = start_time.strftime("%Y%m%dT%H%M%SZ")
            end = end_time.strftime("%Y%m%dT%H%M%SZ")
            start_time += timedelta(days=1)
            end_time += timedelta(days=1)

            event = {
                "event_id": event_id,
                "start_time": start,
                "end_time": end,
                "description": description,
                "location": location,
                "reccurence": rec_id
            }

            events.append(event)
    elif recurrence == "week":
        for i in range(rec_count):
            #increment after to make sure we get initial day
            start = start_time.strftime("%Y%m%dT%H%M%SZ")
            end = end_time.strftime("%Y%m%dT%H%M%SZ")
            start_time += timedelta(days=7)
            end_time += timedelta(days=7)

            event = {
                "event_id": event_id,
                "start_time": start,
                "end_time": end,
                "description": description,
                "location": location,
                "reccurence": rec_id
            }

            events.append(event)
    elif recurrence == "month":
        #for month and year the delta needs to be relative to the initial date, different from day increments
        n_start = start_time
        n_end = end_time
        for i in range(rec_count):
            #increment goes first in this case since we start by adding 0
            n_start = start_time + relativedelta(months=i)
            n_end = end_time + relativedelta(months=i)
            start = n_start.strftime("%Y%m%dT%H%M%SZ")
            end = n_end.strftime("%Y%m%dT%H%M%SZ")
            

            event = {
                "event_id": event_id,
                "start_time": start,
                "end_time": end,
                "description": description,
                "location": location,
                "reccurence": rec_id
            }

            events.append(event)
    elif recurrence == "year":
        n_start = start_time
        n_end = end_time
        for i in range(rec_count):
            n_start = start_time + relativedelta(years=i)
            n_end = end_time + relativedelta(years=i)
            start = n_start.strftime("%Y%m%dT%H%M%SZ")
            end = n_end.strftime("%Y%m%dT%H%M%SZ")

            event = {
                "event_id": event_id,
                "start_time": start,
                "end_time": end,
                "description": description,
                "location": location,
                "reccurence": rec_id
            }

            events.append(event)

    calendar_db.append_event_list(username,events)
    calendar_db.inc_rec_id(username)
    #calendar_db.update_event_list(username,events)


#MVC Wrappers for DB functions

def create_user(username, password, first_name, last_name):
    calendar_db.create_user(username, password, first_name, last_name)

def edit_user(username, password=None, first_name=None, last_name=None):
    calendar_db.edit_user(username, password, first_name, last_name)

def find_user(username):
    return calendar_db.find_user(username)

def create_event(username, event_id, start_time, end_time, description=None, location=None,recurrence=0):
    calendar_db.create_event(username, event_id, start_time, end_time, description, location,recurrence)

def edit_event(username, event_id, start_time, end_time, new_id=None,new_start=None,new_end=None,new_desc=None,new_loc=None,delete=False):
    calendar_db.edit_event(username, event_id, start_time, end_time, new_id,new_start,new_end,new_desc,new_loc,delete)

def add_friend(username, f_username):
    #check friend list for duplicate, if not, add
    if friend_check(username,f_username):
        calendar_db.add_friend(username,f_username)


def remove_friend(username, f_username):
    calendar_db.remove_friend(username, f_username)

def get_friends(username):
    return calendar_db.get_friends(username)["friends"]


#eastern = timezone('US/Eastern')

#print( datetime.now(pytz.utc))
#export_calendar( "Billy", "csv", eastern )


#print(pytz.common_timezones_set)

#western = timezone('US/Pacific')
#strftime("%Y%m%dT%H%M%SZ")
#print(datetime.now(pytz.utc).astimezone(eastern).strftime("%Y"))


# print(pytz.common_timezones_set)
# eastern = timezone('US/Eastern')
# western = timezone('US/Pacific')
# strftime("%Y%m%dT%H%M%SZ")
# print(datetime.now(pytz.utc).astimezone(eastern).strftime("%Y"))

# print(get_event_list("Billy",eastern))
# 20210906T110000
# 20211021T140000
# 2021110­­3T183000
# print(get_event_list("testery",eastern,start= "20211020T140000",end="20211023T140000"))
# print(convert_date_input("2021","10","21","8","00",eastern))

# print(get_time_delta("20211021T140000","20211123T150000"))


#add_friend("testery","tdoe")

#add_friend("testery","tdoe")

#please dont flame giant test string ty

# ics_string = """BEGIN:VCALENDAR
# VERSION:2.0
# PRODID:-//calendarplusplus export//
# BEGIN:VEVENT
# SUMMARY:Computer Science Senior Project
# DTSTART:20210906T070000
# DTEND:20210906T081500
# DTSTAMP;VALUE=DATE-TIME:20211209T045712Z

# END:VEVENT
# BEGIN:VEVENT
# SUMMARY:Computer Science Senior Project
# DTSTART:20210913T070000
# DTEND:20210913T081500
# DTSTAMP;VALUE=DATE-TIME:20211209T045712Z
# DESCRIPTION:McKee class
# LOCATION:Robinson 207
# END:VEVENT
# END:VCALENDAR"""

# csv_string = """Subject,Start Date,Start Time,End Date,End Time,Description,Location
# 0A,10/21/2021,08:00,10/21/2021,09:00,,test location (optional?)
# 1A,10/21/2021,10:00,10/21/2021,11:00,a second test event,maybe a location"""

# print(import_calendar("testery",csv_string,"ics",eastern))

#DTSTART:20210906T070000

#create_rec_event("testery","rec_event_test", "20211031T070000","20211031T081500","month",2,"rec testing", "recland")
