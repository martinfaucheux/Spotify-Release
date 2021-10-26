from django.contrib import admin

from .models import Album, Artist, SpotifyToken


class AlbumInline(admin.TabularInline):
    model = Album.artists.through


class DefaultModelAdmin(admin.ModelAdmin):
    pass


class ArtistAdmin(admin.ModelAdmin):
    inlines = [AlbumInline]


admin.site.register(Artist, ArtistAdmin)
admin.site.register(Album, DefaultModelAdmin)
admin.site.register(SpotifyToken, DefaultModelAdmin)
