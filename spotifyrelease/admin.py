from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path
from rest_framework.authtoken.models import Token

from .models import Album, Artist, SpotifyToken, User
from .tasks import pull_new_release


class AlbumInline(admin.TabularInline):
    model = Album.artists.through


class SpotifyTokenInline(admin.TabularInline):
    model = SpotifyToken


class TokenInline(admin.TabularInline):
    model = Token


class DefaultModelAdmin(admin.ModelAdmin):
    pass


class ArtistAdmin(admin.ModelAdmin):
    inlines = [AlbumInline]


class AlbumAdmin(admin.ModelAdmin):
    change_list_template = "spotifyrelease/album_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path("pull-releases/", self.pull_releases),
        ]
        return my_urls + urls

    def pull_releases(self, request):
        pull_new_release()
        self.message_user(request, "New releases have been fetched!")
        return HttpResponseRedirect("../")


class UserAdmin(admin.ModelAdmin):
    inlines = [TokenInline, SpotifyTokenInline]


admin.site.register(Artist, ArtistAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(SpotifyToken, DefaultModelAdmin)
admin.site.register(User, UserAdmin)
