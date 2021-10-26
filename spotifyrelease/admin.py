from django.contrib import admin

from .models import SpotifyToken


class SpotifyTokenAdmin(admin.ModelAdmin):
    pass



admin.site.register(SpotifyToken, SpotifyTokenAdmin)
