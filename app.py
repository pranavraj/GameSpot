import os
from flask import Flask, redirect, url_for, render_template, session, flash
from flask_bootstrap import Bootstrap
from social_profile import ALLOWED_SOCIAL_PROFILES, SocialProfile

from dotenv import load_dotenv
load_dotenv("verbose=True")

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersekrit")

for profile in ALLOWED_SOCIAL_PROFILES:
    profile.register_app(app)

Bootstrap(app)

########################
# Login/ Logout function
########################

@app.route("/login/<profileObject>")
def login(profileObject):
    if not profile.is_authorized():
        return redirect(url_for(profile.get_authorization_url()))
    profile.login()
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    if "profile" in session:
        del session["profile"]
    flash("Successfully logged out")
    return redirect(url_for("index"))


##################
# Home page
##################

@app.route("/home")
@app.route("/")
def index():

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

