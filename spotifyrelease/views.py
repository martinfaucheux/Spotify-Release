from django.http import HttpResponseRedirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from utils.pagination import CustomPagination
from utils.spotify_auth import SpotifyAuth
from utils.spotify_browser import fetch_new_release_data

from spotifyrelease.models import Album, Artist, SpotifyToken
from spotifyrelease.serializers import AlbumSerializer, ArtistSerializer


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
