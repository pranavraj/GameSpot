import datetime
import os
from mongoengine import *



#todo define class objects for these collections

def add_user_if_not_present(profile):

    profile_type = profile.profile_type
    profile_user_email = profile.email
    existing_users_count = db.Users.count_documents({"email": profile_user_email, "type": profile_type})

    if existing_users_count == 0:
        db.Users.insert_one(
            {
                "email" : profile_user_email,
                "type" : profile_type,
                "name" : profile.name,
                "shardKey": profile_type,
                "createdLeagues": [],
                "games": [],
                "joinedLeagues" : []
            }
        )

def get_user(profile):
    
    profile_type = profile.profile_type
    profile_user_email = profile.email
    users = db.Users.find({"email": profile_user_email, "type": profile_type})
    if users:
        return users[0]
    return None







