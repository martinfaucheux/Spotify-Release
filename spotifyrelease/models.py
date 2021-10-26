from django.db import models
from django.utils import timezone
from utils.model_mixins import TimeStampMixin
from utils.spotify_auth import SpotifyAuth

from .constants import AlbumType


class Artist(TimeStampMixin):
    spotify_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name if self.name else f"Artist {self.id}"


class Album(TimeStampMixin):
    spotify_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    album_type = models.CharField(
        choices=AlbumType.CHOICES, default=AlbumType.ALBUM, max_length=255
    )
    release_date = models.DateTimeField(blank=True, null=True)

    artists = models.ManyToManyField(Artist, related_name="albums")

    def __str__(self):
        return self.name if self.name else f"Album {self.id}"


class SpotifyToken(TimeStampMixin):

    access_token = models.CharField(blank=True, max_length=255)
    refresh_token = models.CharField(blank=True, max_length=255)
    expire_at = models.DateTimeField()

    @property
    def is_valid(self):
        return timezone.now() < self.expire_at

    def refresh(self):
        auth_manager = SpotifyAuth()
        token_data = auth_manager.refresh_auth(self.refresh_token)

        if token_data is not None:
            save_kwargs = auth_manager.get_save_kwargs(token_data)
            for field, value in save_kwargs.items():
                setattr(self, field, value)
            self.save()

        else:
            raise Exception("Could not refresh the token")
