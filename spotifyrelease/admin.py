from django.contrib import admin

from .models import Album, Artist, SpotifyToken


class DefaultModelAdmin(admin.ModelAdmin):
    pass


admin.site.register(Artist, DefaultModelAdmin)
admin.site.register(Album, DefaultModelAdmin)
admin.site.register(SpotifyToken, DefaultModelAdmin)
