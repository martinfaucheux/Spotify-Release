import base64
import json
from datetime import timedelta

import requests
from config import settings
from django.utils import timezone

SPOTIFY_URL_AUTH = "https://accounts.spotify.com/authorize/"
SPOTIFY_URL_TOKEN = "https://accounts.spotify.com/api/token/"
SPOTIFY_URL_USER_INFO = "https://api.spotify.com/v1/me/"

RESPONSE_TYPE = "code"
CONTENT_TYPE = "application/x-www-form-urlencoded"
SCOPE = "user-read-email user-read-private"


class SpotifyAuth(object):

    CLIENT_ID = settings.SPOTIFY_CLIENT_ID
    CLIENT_SECRET = settings.SPOTIFY_CLIENT_SECRET
    CALLBACK_URL = settings.SPOTIFY_CALLBACK_URL

    def refresh_auth(self, refresh_token):
        body = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": self.CLIENT_ID,
            "client_secret": self.CLIENT_SECRET,
        }
        headers = {"Content-Type": CONTENT_TYPE}

        post_refresh = requests.post(SPOTIFY_URL_TOKEN, data=body, headers=headers)
        p_back = json.loads(post_refresh.text)

        return self._handle_token(p_back)

    def get_oauth_url(self):
        return self._get_auth(
            self.CLIENT_ID,
            self.CALLBACK_URL,
            SCOPE,
        )

    def get_user_token(self, code):
        return self._get_token(
            code, self.CLIENT_ID, self.CLIENT_SECRET, self.CALLBACK_URL
        )

    def get_save_kwargs(self, token_data):
        kwargs = {
            k: v
            for k, v in token_data.items()
            if k in ["access_token", "refresh_token"]
        }
        expires_in = token_data["expires_in"]
        kwargs["expire_at"] = timezone.now() + timedelta(seconds=expires_in)
        return kwargs

    def get_user_info(self, access_token):
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        request = requests.get(SPOTIFY_URL_USER_INFO, headers=headers)
        user_info = json.loads(request.text)

        if "error" in user_info:
            raise Exception("Could not fetch user data")

        return {"name": user_info["display_name"], "email": user_info["email"]}

    def _get_auth(self, client_id, redirect_uri, scope):
        return (
            f"{SPOTIFY_URL_AUTH}"
            f"?client_id={client_id}"
            f"&redirect_uri={redirect_uri}"
            f"&scope={scope}"
            "&response_type=code"
        )

    def _get_token(self, code, client_id, client_secret, redirect_uri):
        body = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
            "client_id": client_id,
            "client_secret": client_secret,
        }

        encoded = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
        headers = {
            "Content-Type": CONTENT_TYPE,
            "Authorization": f"Basic {encoded}",
        }

        post = requests.post(SPOTIFY_URL_TOKEN, params=body, headers=headers)
        return self._handle_token(json.loads(post.text))

    def _handle_token(self, response):
        if "error" in response:
            return None

        return {
            key: value
            for key, value in response.items()
            if key in ["access_token", "expires_in", "refresh_token"]
        }
