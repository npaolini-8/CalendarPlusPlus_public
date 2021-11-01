from pymongo import MongoClient # MongoDB Library to connect to database.
from datetime import datetime, tzinfo # Used to get timestamps for database information
import ssl # Used to specify certificate connection for MongoDB

class CalDB():
    def __init__(self):
        self.cluster = MongoClient("mongodb+srv://nickp:UEuYChybyfDeiRRq@cal0.uud0f.mongodb.net/test", ssl_cert_reqs=ssl.CERT_NONE)
        self.cal_db = cluster["calendar"]
        self.users_collection = cal_db["users"]

    def create_user( self, username, password, first_name, last_name):
        self.users_collection.insert_one(
            {
                "username": username,
                "password": password,
                "first_name": first_name,
                "last_name": last_name,
                "events": [],
                "friends": []
            }
    )

    def create_event(self,username, event_id, start_time, end_time, description, location, recurrence): # we should use the date-time format used by ical for easier maintenance and conversion
        self.users_collection.update_one(
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

    def add_friend( self, username, f_username):
        self.users_collection.update_one(
            {"username": username},
            {"$push":
                {"friends":
                    {
                        "username": f_username
                    }
                }
            }
    )