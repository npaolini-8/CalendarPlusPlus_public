from os import write
from pymongo import MongoClient # MongoDB Library to connect to database.
from datetime import datetime, tzinfo # Used to get timestamps for database information
import ssl # Used to specify certificate connection for MongoDB
from icalendar import Calendar, Event
import pytz
from typing import List
import csv


cluster = MongoClient("mongodb+srv://nickp:UEuYChybyfDeiRRq@cal0.uud0f.mongodb.net/test", ssl_cert_reqs=ssl.CERT_NONE)
cal_db = cluster["calendar"]
users_collection = cal_db["users"]

def create_user( username, password, first_name, last_name):
    users_collection.insert_one(
        {
            "username": username,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "events": [],
            "friends": []
        }
    )

def create_event(username, event_id, start_time, end_time, description, location, recurrence): # we should use the date-time format used by ical for easier maintenance and conversion
    users_collection.update_one(
        {"username": username},
        {"$push":
            {"events":
                {
                    "event_id": event_id,
                    #"event_date": event_date, wrapping into datetime
                    "start_time": start_time,
                    "end_time": end_time,
                    "description": description,
                    "location": location,
                    "recurrence": recurrence
                }
            }
        }

    )

def add_friend( username, f_username):
    users_collection.update_one(
        {"username": username},
        {"$push":
            {"friends":
                {
                    "username": f_username
                }
            }
        }
    )

#builds calendar file based on given format: ics, csv
def export_calendar( username, format):

    #db queries
    #TODO: Error handling
    user = users_collection.find_one({"username" : username})
    events = user["events"]
    
    if format.lower() == "ics":
        #generate icalendar object from db events
        #TODO: do we want to pass username and build that into ical file description?
        cal = build_ics( events )
        #generates string from ical object
        data = cal.to_ical()

        #writes file
        #TODO: will we ultimately switch this to string return and pass back to front end?
        with open( "export_test/test.ics", 'wb') as ical_file:
            ical_file.write(data)
    
    elif format.lower() == "csv" :
        csv_cal = build_csv( events )

        with open( "export_test/test.csv", 'w', encoding='utf-8') as csv_handler:
            writer = csv.writer(csv_handler)
            
            for row in csv_cal:
                writer.writerow([r.strip('[]')] for r in row)
        

def build_ics( events ) -> Calendar:

    cal = Calendar()
    id = 0

    #required header for compatibility
    cal.add('version', '2.0')
    cal.add('prodid', '-//calendarplusplus export//') #can put anything here wrapped in the slashes i think...

    #icals are populated by event subcomponents, loop builds event subcomponents from DB and adds them to calendar
    for item in events:
        event = Event()

        event.add( 'uid', str(id))
        id += 1

        date = get_datetime(item["start_time"])
        event.add('dtstart', date)

        date = get_datetime(item["end_time"])
        event.add('dtend', date)

        event.add('description', item["description"])
        cal.add_component(event)

    return cal

#returns datetime object built from datetime string from db
#format: YYYYMMDDTHHMMSS
#assumes we are storing in utc, tags objects accordingly
def get_datetime( datestr ) -> datetime:

    year = int(datestr[0:4])
    month = int(datestr[4:6])
    day = int(datestr[6:8])

    hour = int(datestr[9:11])
    minute = int(datestr[11:13])

    return datetime(year,month,day,hour,minute, tzinfo=pytz.utc)


def build_csv( events):

    csv_data : List[List[str]] = []

    #add header
    #TODO: format?
    row = ["Description", "Start", "End","Location","Recurrence"]
    csv_data.append(row)

    for item in events:
        row = [ item["description"], item["start_time"], item["end_time"], item["location"], str(item["recurrence"])]
        csv_data.append(row)

    return csv_data


export_calendar( "testy", "csv" )

#confirmed working
#create_user("testery","plaintext smile", "Two", "Tester")
#create_event("testy", "1A", "1400", "1500", "a second test event", "maybe a location", 0)
#add_friend("testy","testery")