from flask_dance.contrib.google import make_google_blueprint, google
from flask import session, flash
import os
from database import users

class SocialProfile():

    def register(self, registration_api_response):
        raise Exception("Not implemented")

    def get_oauth_config(self):
        raise Exception("Not implemented")

    def register(self, response):
        raise Exception("Not implemented")

    def make_blueprint(self):
        raise Exception("Not implemented")

    def get_display_name(self):
        raise Exception("Not implemented")

    def is_authorized(self):
        raise Exception("Not implemented")

    def get_authorization_url(self):
        raise Exception("Not implemented")

    def login(self):
        raise Exception("Not implemented")

    def register_app(self, app):
        app.config.update(self.get_oauth_config())
        app.register_blueprint(self.make_blueprint(), url_prefix="/login")

    def get_matching_profile(self):
        for available_profile in ALLOWED_SOCIAL_PROFILES:
            if available_profile.get_display_name() == self.get_display_name():
                return available_profile
        return None

    def _update_session_with_profile(self, profile_info):
        session["profile"] = profile_info
        session["profile_type"] = self.get_display_name()
        session_profile = self.get_matching_profile()
        session_profile.register(profile_info)
        users.add_user_if_not_present(session_profile)

    def get_session_profile():
        if "profile" in session and "profile_type" in session:
            social_profile = [profile for profile in ALLOWED_SOCIAL_PROFILES if profile.get_display_name() == session["profile_type"]][0]
            social_profile.register(session["profile"])
            return social_profile
        return None

class GoogleProfile(SocialProfile):

    def register(self, google_response):
        
        if "error" in google_response:
            raise Exception("Error logging in")
    
        self.name = google_response["given_name"]
        self.image = google_response["picture"]
        self.email = google_response["email"]

    def get_oauth_config(self):
        
        config = {}
        config["GOOGLE_OAUTH_CLIENT_ID"] = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
        config["GOOGLE_OAUTH_CLIENT_SECRET"] = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")
        return config

    def make_blueprint(self):
        return make_google_blueprint(scope=["profile", "email"])

    def get_display_name(self):
        return "Google"
    
    def is_authorized(self):
        return google.authorized
    
    def get_authorization_url(self):
        return "google.login"
    
    def login(self):
        resp = google.get("/oauth2/v1/userinfo").json()
        self._update_session_with_profile(resp)
        flash("Logged in using google email id {}".format(resp["email"]))

ALLOWED_SOCIAL_PROFILES = [
    GoogleProfile()
]