from django.contrib.auth import login as auth_login
from django.http import HttpResponseRedirect
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from utils.pagination import CustomPagination
from utils.spotify_auth import SpotifyAuth
from utils.spotify_browser import fetch_new_release_data

from spotifyrelease.models import Album, Artist, SpotifyToken, User
from spotifyrelease.serializers import AlbumSerializer, ArtistSerializer


# Create your views here.
@api_view(["GET"])
def spotify_auth_callback_view(request):

    code = request.GET.get("code")

    if code is None:
        raise PermissionDenied("No code was passed in the url")
    else:
        auth_manager = SpotifyAuth()
        token_data = auth_manager.get_user_token(code)

        if token_data is None:
            raise PermissionDenied("Could not retrieve token data")
        else:
            save_kwargs = auth_manager.get_save_kwargs(token_data)

            access_token = save_kwargs["access_token"]
            user_info = auth_manager.get_user_info(access_token)

            user, _ = User.objects.get_or_create(
                email=user_info["email"], defaults={"name": user_info["name"]}
            )

            existing_spotify_token = getattr(user, "spotify_token", None)
            if existing_spotify_token is not None:
                existing_spotify_token.delete()

            SpotifyToken.objects.update_or_create(user=user, defaults=save_kwargs)

            auth_token, _ = Token.objects.get_or_create(user=user)
            auth_login(request, user=user)

    return Response(status=status.HTTP_200_OK, data={"token": auth_token.key})


@api_view(["GET"])
def spotify_login_view(request):
    auth_manager = SpotifyAuth()
    url = auth_manager.get_oauth_url()
    return HttpResponseRedirect(redirect_to=url)


@api_view(["GET"])
def display_new_releases(request):
    """
    Test view to fetch raw data from Spotify
    """
    spotify_token = SpotifyToken.objects.order_by("-updated_at").first()

    if not spotify_token.is_valid:
        spotify_token.refresh()

    return Response(
        status=status.HTTP_202_ACCEPTED,
        data=fetch_new_release_data(spotify_token.access_token),
    )


class ArtistViewSet(ReadOnlyModelViewSet):
    serializer_class = ArtistSerializer
    pagination_class = CustomPagination
    queryset = Artist.objects.all()

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name", "created_at"]
    ordering = ["name"]


class AlbumViewSet(ReadOnlyModelViewSet):
    serializer_class = AlbumSerializer
    pagination_class = CustomPagination
    filter_backends = [SearchFilter]
    queryset = Album.objects.all()

    search_fields = ["name"]
    ordering_fields = ["name", "created_at"]
    ordering = ["name"]


class ArtistOfAlbumViewSet(ArtistViewSet):
    def get_queryset(self):
        album_id = self.kwargs.get("album_pk")
        album = get_object_or_404(Album.objects.all(), pk=album_id)
        return album.artists.order_by("name")


class AlbumOfArtistViewSet(AlbumViewSet):
    def get_queryset(self):
        artist_id = self.kwargs.get("artist_pk")
        artist = get_object_or_404(Artist.objects.all(), pk=artist_id)
        return artist.albums.order_by("name")
