import base64
import json

import requests
from config import settings

SPOTIFY_URL_AUTH = "https://accounts.spotify.com/authorize/"
SPOTIFY_URL_TOKEN = "https://accounts.spotify.com/api/token/"
RESPONSE_TYPE = "code"
HEADER = "application/x-www-form-urlencoded"
CALLBACK_URL = "http://localhost:5000/auth"
SCOPE = "user-read-email user-read-private"


class SpotifyAuth(object):

    CLIENT_ID = settings.SPOTIFY_CLIENT_ID
    CLIENT_SECRET = settings.SPOTIFY_CLIENT_SECRET

    def refresh_auth(self, refresh_token):
        body = {"grant_type": "refresh_token", "refresh_token": refresh_token}

        post_refresh = requests.post(SPOTIFY_URL_TOKEN, data=body, headers=HEADER)
        p_back = json.dumps(post_refresh.text)

        return self._handle_token(p_back)

    def get_user(self):
        return self._get_auth(
            self.CLIENT_ID,
            f"{CALLBACK_URL}/callback",
            SCOPE,
        )

    def get_user_token(self, code):
        return self._get_token(
            code, self.CLIENT_ID, self.CLIENT_SECRET, f"{CALLBACK_URL}/callback"
        )

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
            "Content-Type": HEADER,
            "Authorization": f"Basic {encoded}",
        }

        post = requests.post(SPOTIFY_URL_TOKEN, params=body, headers=headers)
        return self._handle_token(json.loads(post.text))

    def _handle_token(self, response):
        if "error" in response:
            return response
        return {
            key: response[key]
            for key in ["access_token", "expires_in", "refresh_token"]
        }
