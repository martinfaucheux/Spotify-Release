from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from utils.exceptions import InvalidSpotifyToken
from utils.models import LowerEmailField, TimeStampMixin
from utils.spotify_auth import SpotifyAuth

from .constants import AlbumType
from .managers import UserManager


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

    user = models.OneToOneField(
        "spotifyrelease.User",
        on_delete=models.CASCADE,
        related_name="spotify_token",
        null=True,
        blank=True,
    )

    @property
    def is_valid(self):
        return timezone.now() < self.expire_at

    def refresh(self):
        auth_manager = SpotifyAuth()

        try:
            token_data = auth_manager.refresh_auth(self.refresh_token)
            save_kwargs = auth_manager.get_save_kwargs(token_data)
            for field, value in save_kwargs.items():
                setattr(self, field, value)
            self.save()
        except InvalidSpotifyToken:
            self.user.delete_tokens()
            raise


class User(AbstractUser):
    # Delete unused fields
    username = None
    first_name = None
    last_name = None

    # Use email as username
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # removes email from REQUIRED_FIELDS

    name = models.CharField(max_length=255, null=True, blank=True)
    email = LowerEmailField(
        unique=True, db_index=True, help_text="Email of the user"
    )  # changes email to unique and blank to false

    objects = UserManager()

    def delete_tokens(self):
        for attr_name in ["spotify_token", "auth_token"]:
            token = getattr(self, attr_name, None)
            if token is not None:
                token.delete()
