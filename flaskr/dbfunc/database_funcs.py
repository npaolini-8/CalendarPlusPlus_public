from pymongo import MongoClient  # MongoDB Library to connect to database.
#from datetime import datetime, tzinfo  # Used to get timestamps for database information
import ssl  # Used to specify certificate connection for MongoDB
import random,string

#NOTE: if i were do this again i would leave start and end times in discrete fields for easier querying and sorting
#      would also give events an ID outside of name

class CalDB():
    def __init__(self):
        self.cluster = MongoClient("mongodb+srv://<USERNAME>:<PASSWORD>@cal0.uud0f.mongodb.net/test",
                                   ssl_cert_reqs=ssl.CERT_NONE)
        self.cal_db = self.cluster["calendar"]
        self.users_collection = self.cal_db["users"]

    def generate_salt(self):
        return "".join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(32))

    def create_user(self, username, password, salt, first_name, last_name):
        self.users_collection.insert_one(
            {
                "username": username,
                "password": password,
                "first_name": first_name,
                "last_name": last_name,
                "events": [],
                "friends": [],
                "rec_count": 1,
                "salt":salt
            }
        )

    def find_user(self, username):
        user = self.users_collection.find_one({"username": username},{"password":0,"salt":0})
        return user

    def get_salt(self,username):
        return self.users_collection.find_one({"username":username},{"_id":0,"salt":1})["salt"]

    def auth_user(self, username, hashed_pw):
        return self.users_collection.find_one({"username": username, "password":hashed_pw},{"password":0})

    def check_user(self, username):
        return self.users_collection.find_one({"username": username},{"username":1})


    def edit_user(self, username, password=None, first_name=None, last_name=None):
        edit_dict = {}
        if password is not None:
            edit_dict.update({"password": password})
        if first_name is not None:
            edit_dict.update({"first_name": first_name})
        if last_name is not None:
            edit_dict.update({"last_name": last_name})

        self.items_collection.update_one(
            {"username": username},
            {"$set": edit_dict}
        )

    def create_event(self, username, event_id, start_time, end_time, description=None, location=None,
                     recurrence=0):  # we should use the date-time format used by ical for easier maintenance and conversion
        self.users_collection.update_one(
            {"username": username},
            {"$push":
                {"events":
                    {
                        "event_id": event_id,
                        # "event_date": event_date, wrapping into datetime
                        "start_time": start_time,
                        "end_time": end_time,
                        "description": description,
                        "location": location,
                        "recurrence": recurrence
                    }
                }
            }

        )

    #built delete functionality into edit
    #matching events on id, start, and end time. this combination should be unique, unless user is scheduling
    #duplicate events for some reason
    def edit_event(self, username, event_id, start_time, end_time, new_id=None,new_start=None,new_end=None,new_desc=None,new_loc=None,delete=False):
        
        if delete is not True: #dont bother looking at edit dict if youre deleting
            edit_dict ={}
            if new_id is not None:
                edit_dict.update({"events.$[eventitem].event_id": new_id})
            if new_start is not None:
                edit_dict.update({"events.$[eventitem].start_time": new_start})
            if new_end is not None:
                edit_dict.update({"events.$[eventitem].end_time": new_end})
            if new_desc is not None:
                edit_dict.update({"events.$[eventitem].description": new_desc})
            if new_loc is not None:
                edit_dict.update({"events.$[eventitem].location": new_loc})

        if delete:
            self.users_collection.update_one(
                {
                    "username" : username
                },
                {
                    '$pull': {"events": {"event_id": event_id,"start_time": start_time,"end_time":end_time}}
                }
            )
        else:
            self.users_collection.update_one(
                {
                    "username" : username
                },
                {
                  '$set' :edit_dict
                },
                upsert=False,
                array_filters=[
                    {
                        "eventitem.event_id": event_id,
                        "eventitem.start_time": start_time,
                        "eventitem.end_time": end_time

                    }
                ]
            )

    #start and end params to get events in a given date range, after a start date, or before an end date
    #NOTE range functionality not implemented here, relies on cal_funcs, should be improved in business release
    def get_event_list(self, username, start=None,end=None):

        events = self.find_user(username)["events"]
        return_list = []

        if start is not None and end is not None:
            pass
        elif start is not None:
            pass
        elif end is not None:
            pass
        else:
            return_list = events

        return return_list


    def update_event_list(self, username, events):
        self.users_collection.update_one(
            {"username": username},
            {"$push": {"events": {"$each": events}}}
        )

    #NOTE: Deprecated function, NAMING IS REVERSED, THIS DOES NOT APPEND :(
    def append_event_list(self, username, events):
        self.users_collection.update_one(
            {"username": username},
            {"$set": {"events": events}}
        )

    def add_friend(self, username, f_username):
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
    
    def remove_friend(self, username, f_username):
        self.users_collection.update_one(
            {
                "username": username
            },
            {
                '$pull': {"friends": {"username":f_username}}
            }
        )
    
    def get_friends(self, username):
        return self.users_collection.find_one({"username": username}, {"_id":0,"friends":1})

    def get_rec_id(self,username):
        return self.users_collection.find_one({"username":username}, {"rec_count":1})["rec_count"]

    def inc_rec_id(self,username):
        self.users_collection.update_one({"username":username}, {"$inc": {"rec_count":1}})
