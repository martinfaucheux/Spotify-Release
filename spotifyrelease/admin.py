from django.contrib import admin

from .models import Album, Artist, SpotifyToken, Track


class DefaultModelAdmin(admin.ModelAdmin):
    pass


admin.site.register(Artist, DefaultModelAdmin)
admin.site.register(Track, DefaultModelAdmin)
admin.site.register(Album, DefaultModelAdmin)
admin.site.register(SpotifyToken, DefaultModelAdmin)
