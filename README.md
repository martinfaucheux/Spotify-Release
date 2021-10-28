# Spotify-Release
Django API which pull Spotify new release data

# Usage

## Sign in / Sign up
**GET** `/auth/login`
This will redirect you to the spotify to log in. Spotify will then POST on the callback URL to provide the code.

**POST** `/auth/callback`
Route used by Spotify durint OAuth process. This will get or create a User based on user's Spotify data using the code provided by Spotify in the URL. This returns an authentication token that needs to be passed in subsequent requests.

If the spotify token expires, this will result logging out the user (ie deleting his auth token).

## Objects
You can fetch Album and Artists data pulled from Spotify using the following routes (**GET** only):
* /api/artists/(:id)
* /api/artists/:id/albums/
* /api/albums/(:id)/
* /api/albums/:id/artists

Theses routes require an auth token.

## Fetching new release
Spotify data is pulled periodically with a background job. It uses the first token it founds to make the request.

# App
This code runs on Heroku: http://spotify-pull-release.herokuapp.com/auth/login

New releases are pulled every day automatically.

# Possible improvements

* add tests
* add state and store in the cache to make the OAuth process more secure
* check the Spotify token of all users periodically and delete their auth token if an error happen