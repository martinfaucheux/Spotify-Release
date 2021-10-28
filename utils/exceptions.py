from django.contrib.auth import get_user_model
from rest_framework.exceptions import APIException


class InvalidToken(APIException):
    status_code = 403
    default_detail = "Invalid Spotify Token. Please login again."
    default_code = "invalid_spotify_token"

    def __init__(self, *args, spotify_access_token, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.select_related("auth_token", "spotify_token").get(
                spotify_token__access_token=spotify_access_token
            )
            user.delete_tokens()
        except User.DoesNotExist:
            pass

        super().__init__(*args, **kwargs)
