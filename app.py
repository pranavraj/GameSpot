"""
Entry point for the flask application
"""

import os
from flask import Flask, redirect, url_for, render_template, session, flash
from flask_bootstrap import Bootstrap
from oauthlib.oauth2 import TokenExpiredError, InvalidGrantError
from dotenv import load_dotenv

from social_profile import ALLOWED_SOCIAL_PROFILES, SocialProfile

load_dotenv("verbose=True")

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersekrit")

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
        return redirect(url_for(profile.get_authorization_url()))

    # to catch the issue mentioned here:
    # https://github.com/singingwolfboy/flask-dance/issues/35
    try:
        profile.login()
    except (InvalidGrantError, TokenExpiredError):
        return redirect(url_for(profile.get_authorization_url()))

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
