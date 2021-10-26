from django.db import models
from utils.model_mixins import TimeStampMixin

from .constants import AlbumType


class Artist(TimeStampMixin):
    spotify_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)


class Track(TimeStampMixin):
    spotify_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)


class Album(TimeStampMixin):
    spotify_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    album_type = models.CharField(
        choices=AlbumType.CHOICES, default=AlbumType.ALBUM, max_length=255
    )
    # release_date = models.DateTimeField()

    artists = models.ManyToManyField(Artist)
    tracks = models.ManyToManyField(Track)


class SpotifyToken(TimeStampMixin):

    access_token = models.CharField(blank=True, max_length=255)
    refresh_token = models.CharField(blank=True, max_length=255)
    expire_at = models.DateTimeField()
