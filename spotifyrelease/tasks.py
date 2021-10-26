from config import celery_app
from utils.spotify_browser import fetch_new_release_data

from .models import Album, Artist, SpotifyToken


@celery_app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")


@celery_app.task()
def pull_new_release():
    token = SpotifyToken.objects.first()

    if token is None:
        raise Exception("No valid token found. Impossible to fetch new releases.")

    if not token.is_valid:
        token.refresh()

    new_release_data = fetch_new_release_data(token.access_token)

    for album_data in new_release_data:

        album_obj, _ = Album.objects.get_or_create(
            spotify_id=album_data["id"],
            defaults={
                "name": album_data["name"],
                "album_type": album_data["album_type"],
            },
        )

        for artist_data in album_data.get("artists", []):
            artist_obj, _ = Artist.objects.get_or_create(
                spotify_id=artist_data["id"], defaults={"name": artist_data["name"]}
            )
            album_obj.artists.add(artist_obj)
