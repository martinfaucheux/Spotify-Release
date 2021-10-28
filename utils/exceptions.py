from rest_framework.exceptions import APIException


class InvalidSpotifyToken(APIException):
    status_code = 403
    default_detail = "Invalid Spotify Token. Please login again."
    default_code = "invalid_spotify_token"
