from datetime import timedelta

from django.http import HttpResponseRedirect
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from utils.spotify_auth import SpotifyAuth

from spotifyrelease.models import SpotifyToken


# Create your views here.
@api_view(["GET"])
def spotify_auth_callback_view(request):

    code = request.GET.get("code")

    if code is not None:
        auth_manager = SpotifyAuth()

        token_data = auth_manager.get_user_token(code)

        if token_data is not None:
            access_token = token_data["access_token"]
            expires_in = token_data["expires_in"]
            refresh_token = token_data["refresh_token"]

            expiration_date = timezone.now() + timedelta(seconds=expires_in)

            SpotifyToken.objects.create(
                access_token=access_token,
                refresh_token=refresh_token,
                expire_at=expiration_date,
            )

    return Response(status=status.HTTP_200_OK, data={"status": "ok"})


@api_view(["GET"])
def spotify_login_view(request):
    auth_manager = SpotifyAuth()
    url = auth_manager.get_user()
    return HttpResponseRedirect(redirect_to=url)
