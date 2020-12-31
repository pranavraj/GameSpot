"""
Entry point for the flask application
"""

import os
from flask import Flask, redirect, url_for, render_template, session, flash
from flask_bootstrap import Bootstrap
from oauthlib.oauth2 import TokenExpiredError, InvalidGrantError
from dotenv import load_dotenv
from flask_mongoengine import MongoEngine

from social_profile import ALLOWED_SOCIAL_PROFILES, SocialProfile

load_dotenv("verbose=True")

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersekrit")

app.config["MONGODB_HOST"] = 'game-spot.mongo.cosmos.azure.com'
app.config["MONGODB_PORT"] = 10255
app.config["MONGODB_DATABASE"] = 'GameSpot'
app.config["MONGODB_USERNAME"] = 'game-spot'
app.config["MONGODB_PASSWORD"] = 'zgbKaOx61vlWFwujG0zL0TJfnHFdn1dpQlrD0x9fbLQtHHSFyvfk4QRboAxEfx6nYD3TD73ndG66N1dNKOdL9w=='

db = MongoEngine(app)

for allowed_profile in ALLOWED_SOCIAL_PROFILES:
    allowed_profile.register_app(app)

Bootstrap(app)

########################
# Login/ Logout function
########################

@app.route("/login/<profile_type>")
def login(profile_type):
    """
    Logs in the user
    - profile_type: The type of profile used for logging in
                    (eg:  Google, facebok)
    """

    profile = SocialProfile.get_matching_profile(profile_type)

    if not profile.is_authorized():
        return redirect(url_for(profile.authorization_url))

    # to catch the issue mentioned here:
    # https://github.com/singingwolfboy/flask-dance/issues/35
    try:
        profile.login()
    except (InvalidGrantError, TokenExpiredError):
        return redirect(url_for(profile.authorization_url))

    #User(name="test1", email="pranav090333333@").save_if_not_present()

    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    """
    Logs the user out
    """
    if "profile" in session:
        del session["profile"]
    flash("Successfully logged out")
    return redirect(url_for("index"))



@app.route("/home")
@app.route("/")
def index():
    """
    Home page rendering logic
    """

    logged_in_user_name = None
    logged_in_user_image = None
    leagues_hosted_by_user = []

    session_profile = SocialProfile.get_session_profile()

    if session_profile:
        logged_in_user_name = session_profile.name
        logged_in_user_image = session_profile.image

    return render_template(
        "homepage.html",
        logged_in_user_name = logged_in_user_name,
        logged_in_user_image = logged_in_user_image,
        leagues_hosted_by_user = leagues_hosted_by_user,
        allowed_profiles = ALLOWED_SOCIAL_PROFILES
    )

from models import User, Game, League