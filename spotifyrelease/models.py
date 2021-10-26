from django.db import models
from django.utils import timezone
from utils.model_mixins import TimeStampMixin
from utils.spotify_auth import SpotifyAuth

from .constants import AlbumType


class Artist(TimeStampMixin):
    spotify_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Album(TimeStampMixin):
    spotify_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    album_type = models.CharField(
        choices=AlbumType.CHOICES, default=AlbumType.ALBUM, max_length=255
    )
    artists = models.ManyToManyField(Artist)

    def __str__(self):
        return self.name


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
