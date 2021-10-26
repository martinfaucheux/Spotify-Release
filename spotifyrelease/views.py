from django.http import HttpResponseRedirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from utils.spotify_auth import SpotifyAuth


# Create your views here.
@api_view(["GET"])
def spotify_auth_callback_view(request):

    # from pprint import pprint
    # pprint(request.data)

    code = request.GET.get("code")

    if code is not None:
        # TODO: to stuff
        print(code)

    return Response(status=status.HTTP_200_OK, data={"status": "ok"})


@api_view(["GET"])
def spotify_login_view(request):
    auth_manager = SpotifyAuth()
    url = auth_manager.get_user()
    return HttpResponseRedirect(redirect_to=url)
