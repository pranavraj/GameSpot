from datetime import datetime
import pymongo
import os


def database_property(property):
    property.is_database_property = True
    return property

class Database():

    def __init__(self, database_name = "GameSpot"):
        uri = os.environ["DATABASE_CONNECTION_STRING"]
        client = pymongo.MongoClient(uri)
        self.db = client[database_name]

    @property
    def updated_date_time(self):
        return datetime.now()
    
    def print_details(self):
        for property, value in dir(self).items():
            print(property, ":", value)