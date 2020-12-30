"""
Module containing all the social profiles
"""

import os
import abc
from flask_dance.contrib.google import make_google_blueprint, google
from flask import session, flash
from database import users

class SocialProfile(metaclass=abc.ABCMeta):
    """
    Base abstract class for social profile classes
    """

    def __init__(self, profile_type):
        self.name = None
        self.image = None
        self.email = None
        self.profile_type = profile_type

    @abc.abstractmethod
    def register(self, registration_api_response):
        """
        Register the social profile object with the
        api response
        """
        pass

    @abc.abstractmethod
    def get_oauth_config(self):
        """
        Returns the oauth config variables as a dictionary
        """
        pass

    @abc.abstractmethod
    def make_blueprint(self):
        """
        Creates blue print to connect with the social profile
        """
        pass

    @abc.abstractmethod
    def is_authorized(self):
        """
        Is authorized to access the social profile
        """
        pass

    @abc.abstractmethod
    def get_authorization_url(self):
        """
        Authorization url
        """
        pass

    @abc.abstractmethod
    def login(self):
        """
        Login using the profile
        """
        pass

    def register_app(self, app):
        """
        Register the app for the profile
        """
        app.config.update(self.get_oauth_config())
        app.register_blueprint(self.make_blueprint(), url_prefix="/login")

    def _update_session_with_profile(self, profile_info):
        """
        Update the session with the profile information
        """
        session["profile"] = profile_info
        session["profile_type"] = self.profile_type
        session_profile = SocialProfile.get_matching_profile(self.profile_type)
        session_profile.register(profile_info)
        users.add_user_if_not_present(session_profile)

    @staticmethod
    def get_matching_profile(profile_type):
        """
        Returns the profile matching the profile_type
        """

        for available_profile in ALLOWED_SOCIAL_PROFILES:
            if available_profile.profile_type == profile_type:
                return available_profile
        return None

    @staticmethod
    def get_session_profile():
        """
        Get the profile stored in the session.
        None if there is not stored profile
        """
        if "profile" in session and "profile_type" in session:
            social_profile = SocialProfile.get_matching_profile(session["profile_type"])
            social_profile.register(session["profile"])
            return social_profile
        return None

class GoogleProfile(SocialProfile):
    """
    Google profile
    """

    def __init__(self):
        SocialProfile.__init__(self, "Google")

    def register(self, registration_api_response):

        if "error" in registration_api_response:
            raise Exception("Error logging in")

        self.name = registration_api_response["given_name"]
        self.image = registration_api_response["picture"]
        self.email = registration_api_response["email"]

    def get_oauth_config(self):

        config = {}
        config["GOOGLE_OAUTH_CLIENT_ID"] = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
        config["GOOGLE_OAUTH_CLIENT_SECRET"] = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")
        return config

    def make_blueprint(self):
        return make_google_blueprint(scope=["profile", "email"])

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
