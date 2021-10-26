"""newrelease URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework_nested import routers
from spotifyrelease.views import (
    AlbumOfArtistViewSet,
    AlbumViewSet,
    ArtistOfAlbumViewSet,
    ArtistViewSet,
    display_new_releases,
    spotify_auth_callback_view,
    spotify_login_view,
)

# Create a router and register our viewsets with it.
router = routers.SimpleRouter()
router.register("artists", ArtistViewSet)
router.register("albums", AlbumViewSet)

artist_router = routers.NestedSimpleRouter(router, "artists", lookup="artist")
artist_router.register("albums", AlbumOfArtistViewSet, basename="albums-of-artist")

album_router = routers.NestedSimpleRouter(router, "albums", lookup="album")
album_router.register("artists", ArtistOfAlbumViewSet, basename="artists-of-albums")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("auth/callback/", spotify_auth_callback_view),
    path("auth/spotify-login/", spotify_login_view),
    path("new-releases", display_new_releases),
    path("api/", include(router.urls)),
    path("api/", include(artist_router.urls)),
    path("api/", include(album_router.urls)),
]
