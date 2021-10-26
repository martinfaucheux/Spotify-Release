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
from rest_framework import routers
from spotifyrelease.views import (
    AlbumViewSet,
    ArtistViewSet,
    display_new_releases,
    spotify_auth_callback_view,
    spotify_login_view,
)

# Create a router and register our viewsets with it.
router = routers.DefaultRouter()
router.register(r"artists", ArtistViewSet)
router.register(r"albums", AlbumViewSet)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("auth/callback/", spotify_auth_callback_view),
    path("auth/spotify-login/", spotify_login_view),
    path("new-releases", display_new_releases),
    path("api/", include(router.urls)),
]
