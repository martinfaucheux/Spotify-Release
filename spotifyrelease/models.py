from django.db import models
from utils.model_mixins import TimeStampMixin


class SpotifyToken(TimeStampMixin):

    access_token = models.CharField(blank=True, max_length=255)
    refresh_token = models.CharField(blank=True, max_length=255)
    expire_at = models.DateField()
