from .utilities import get_db

def add_user_if_not_present(profile):

    profile_type = profile.get_display_name()
    profile_user_email = profile.email

    db = get_db()

    existing_users_count = db.Users.count_documents({"email": profile_user_email, "type": profile_type})

    if existing_users_count == 0:
        print("Adding user {} to database".format(profile.name))
        db.Users.insert_one(
            {
                "email" : profile_user_email,
                "type" : profile_type,
                "name" : profile.name,
                "shardKey": profile_type
            }
        )

