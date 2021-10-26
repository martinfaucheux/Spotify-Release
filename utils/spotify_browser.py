import json

import requests

SPOTIFY_URL_BROWSE = "https://api.spotify.com/v1/browse/new-releases"


# curl --request GET \
#   --url https://api.spotify.com/v1/browse/new-releases \
#   --header 'Authorization: ' \
#   --header 'Content-Type: application/json'


def fetch_new_release_data(access_token):

    album_list = []

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    next_page_url = SPOTIFY_URL_BROWSE

    while next_page_url:
        request = requests.get(url=next_page_url, headers=headers)

        if request.status_code == 200:

            data = json.loads(request.text)["albums"]

            items = data.get("items", [])
            album_list += items

            next_page_url = data.get("next")
        else:
            raise request.raise_for_status()

    return album_list
