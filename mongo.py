from pymongo import MongoClient # MongoDB Library to connect to database.
from datetime import datetime # Used to get timestamps for database information
import ssl # Used to specify certificate connection for MongoDB


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

def create_event(username, event_id, event_date, start_time, end_time, recurrence):
    users_collection.update_one(
        {"username": username},
        {"$push":
            {"events":
                {
                    "event_id": event_id,
                    "event_date": event_date,
                    "start_time": start_time,
                    "end_time": end_time,
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

#confirmed working
#create_user("testery","plaintext smile", "Two", "Tester")
#create_event("testy", "0A","somedate", "1200", "1300", 0)
#add_friend("testy","testery")