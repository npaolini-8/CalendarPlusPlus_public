from os import write
from pymongo import MongoClient # MongoDB Library to connect to database.
from datetime import datetime # Used to get timestamps for database information
import ssl # Used to specify certificate connection for MongoDB
from icalendar import Calendar, Event


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

def export_calendar( username, format):
    user = users_collection.find_one({"username" : username})
    events = user["events"]
    
    if format.lower() == "ics":
        cal = build_ics( events )
        data = cal.to_ical()

        with open( "export_test/test.ics", 'w') as ical_file:
            ical_file,write(data)
    
    else:
        build_csv( events )

    # for event in events:
    #     print( event["event_id"] )
        

def build_ics( events ) -> Calendar:

    cal = Calendar()
    id = 0

    for item in events:
        event = Event()

        event.add( 'uid', str(id))
        id += 1

        event.add('dtstart', datetime(item["start_time"]))
        event.add('dtend', datetime(item["end_time"]))
        event.add('description', item["description"])
        cal.add_component(event)

    return cal

def build_csv( events):
    return None


export_calendar( "testy", "ics" )

#confirmed working
#create_user("testery","plaintext smile", "Two", "Tester")
#create_event("testy", "1A", "1400", "1500", "a second test event", "maybe a location", 0)
#add_friend("testy","testery")