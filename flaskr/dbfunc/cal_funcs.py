from os import write
from datetime import datetime, tzinfo
from re import split # Used to get timestamps for database information
from icalendar import Calendar, Event
import pytz
import csv
from database_funcs import CalDB

calendar_db = CalDB()

#builds calendar file based on given format: ics, csv
def export_calendar( username, format):

    #db queries
    #TODO: Error handling
    user = calendar_db.find_user(username)
    events = user["events"]
    
    if format.lower() == "ics":
        #generate icalendar object from db events
        #TODO: do we want to pass username and build that into ical file description?
        cal = build_ics( events )
        #generates string from ical object
        data = cal.to_ical()

        print(data)

        #writes file
        #TODO: will we ultimately switch this to string return and pass back to front end?
        with open( "export_test/test.ics", 'wb') as ical_file:
            ical_file.write(data)
    
    elif format.lower() == "csv" :
        csv_cal = build_csv( events )

        with open( "export_test/test.csv", 'w', encoding='utf-8') as csv_handler:
            writer = csv.writer(csv_handler)
            
            for row in csv_cal:
                print(row)
                writer.writerow(row)
        

def build_ics( events ) -> Calendar:

    cal = Calendar()
    id = 0

    #required header for compatibility
    cal.add('version', '2.0')
    cal.add('prodid', '-//calendarplusplus export//') #can put anything here wrapped in the slashes i think...

    #icals are populated by event subcomponents, loop builds event subcomponents from DB and adds them to calendar
    for item in events:
        event = Event()

        #event.add( 'uid', str(id))
        id += 1

        date = get_datetime(item["start_time"])
        event.add('dtstart', date)

        date = get_datetime(item["end_time"])
        event.add('dtend', date)

        #adds datestamp for format compliance
        #TODO: do we want to save datestemp (when event was added) in our db?
        event.add('dtstamp', datetime.now(pytz.utc) )

        event.add('summary', item["event_id"])

        #accounting for optional fields
        if item["description"] is not None:
            event.add('description', item["description"])

        if item["location"] is not None:
            event.add('location', item["location"])

        cal.add_component(event)

    return cal

#returns datetime object built from datetime string from db
#format: YYYYMMDDTHHMMSS
#assumes we are storing in utc, tags objects accordingly
def get_datetime( datestr ) -> datetime:

    # year = int(datestr[0:4])
    # month = int(datestr[4:6])
    # day = int(datestr[6:8])

    # hour = int(datestr[9:11])
    # minute = int(datestr[11:13])

    date_components = get_date_components(datestr)

    #return datetime(year,month,day,hour,minute, tzinfo=pytz.utc)
    return datetime(int(date_components[0]), int(date_components[1]), int(date_components[2]), int(date_components[3]), int(date_components[4]), tzinfo=pytz.utc)

def get_date_components( datestr ):

    year = datestr[0:4]
    month = datestr[4:6]
    day = datestr[6:8]

    hour = datestr[9:11]
    minute = datestr[11:13]

    return [year,month,day,hour,minute]




def build_csv( events):

    #csv_data : List[List[str]] = []
    csv_data = []

    #add header
    row = ["Subject", "Start Date", "Start Time", "End Date", "End Time","Description","Location"]
    csv_data.append(row)

    for item in events:
        #TODO: Timezone in google csv? Are we going to get this from front end?
        start_components = get_date_components(item["start_time"])
        end_components = get_date_components(item["end_time"])

        start_date = start_components[1] + "/" + start_components[2] + "/" + start_components[0]
        start_time = start_components[3] + ":" + start_components[4]

        end_date = end_components[1] + "/" + end_components[2] + "/" + end_components[0]
        end_time = end_components[3] + ":" + end_components[4]

        row = [ item["event_id"], start_date, start_time, end_date, end_time]

        #accounting for optional fields again
        if item["description"] is not None:
            row.append(item["description"])
        
        if item["location"] is not None:
            row.append(item["location"])

        csv_data.append(row)

    #print(csv_data)
    return csv_data


#TODO: add accounting for optional fields
def import_calendar( username, cal_str, format ):

    #assuming string input from app this file read would simply stay as variable input
    #file read done for testing

    events = calendar_db.find_user(username)["events"]

    if format == "ics":

        cal = Calendar()

        cal_file = open("export_test/test.ics", 'r')
        cal_str = cal_file.read()
        components = cal.from_ical(cal_str)

        #strftime string is formatted string output from datetime object to match current convention
        #source: https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
        for component in components.walk():
            if component.name == "VEVENT":
                # print(component.get('summary'))
                # print(component.get('dtstart').dt.astimezone(pytz.utc).strftime("%Y%m%dT%H%M%SZ"))
                # print(component.decoded('dtstart'))
                # print(component.get('dtend').dt.astimezone(pytz.utc).strftime("%Y%m%dT%H%M%SZ"))
                
                events.append({"event_id":component.get('summary'),"start_time":component.get('dtstart').dt.astimezone(pytz.utc).strftime("%Y%m%dT%H%M%SZ"),\
                     "end_time":component.get('dtend').dt.astimezone(pytz.utc).strftime("%Y%m%dT%H%M%SZ"), "description":component.get('description'),  "location":component.get('location')})

    #TODO: timezone again for google csv format, not sure if it is ever listed. we may need to "assume" based on selected timezone of current user
    #TODO: this works for expected format of subject, start date, start time, end date, end time, description, and location, need to test for other cases
    elif format == "gcsv":
        with open("export_test/test.csv", 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)

            for row in csv_reader:
                subj = row['Subject']

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
                start_string = start_dt.strftime("%Y%m%dT%H%M%SZ")

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
                end_string = end_dt.strftime("%Y%m%dT%H%M%SZ")

                desc = row['Description']
                loc = row['Location']

                events.append({"event_id": subj,"start_time": start_string,"end_time": end_string,"description": desc, "location": loc })

    calendar_db.update_event_list(username,events)

#print( datetime.now(pytz.utc))
#export_calendar( "testy", "ics" )
#import_calendar("testery","test","gcsv")
