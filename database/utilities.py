

import pymongo
import os

def get_db():

    uri = os.environ["DATABASE_CONNECTION_STRING"]
    client = pymongo.MongoClient(uri)
    db = client.GameSpot
    return db