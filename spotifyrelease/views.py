from django.http import HttpResponseRedirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from utils.spotify_auth import SpotifyAuth
from utils.spotify_browser import fetch_new_release_data

from spotifyrelease.models import SpotifyToken


# Create your views here.
@api_view(["GET"])
def spotify_auth_callback_view(request):

    code = request.GET.get("code")

    if code is not None:
        auth_manager = SpotifyAuth()
        token_data = auth_manager.get_user_token(code)

        if token_data is not None:
            save_kwargs = auth_manager.get_save_kwargs(token_data)
            SpotifyToken.objects.create(**save_kwargs)

    return Response(status=status.HTTP_200_OK, data={"status": "ok"})


@api_view(["GET"])
def spotify_login_view(request):
    auth_manager = SpotifyAuth()
    url = auth_manager.get_user()
    return HttpResponseRedirect(redirect_to=url)


@api_view(["GET"])
def display_new_releases(request):
    spotify_token = SpotifyToken.objects.order_by("-updated_at").first()

    if not spotify_token.is_valid:
        spotify_token.refresh()

    return Response(
        status=status.HTTP_202_ACCEPTED,
        data=fetch_new_release_data(spotify_token.access_token),
    )
