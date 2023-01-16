import os
from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials


def get_billboard_tracks(url):
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(e)

    if response:
        # Make response data into a soup object.
        top_100_web_page = response.text
        soup = BeautifulSoup(top_100_web_page, "html.parser")
        songs = soup.find_all(class_="o-chart-results-list-row-container")

        # Add the tracks and artists into list.
        tracks_and_artists = [
            {"track": song.find(name="h3").text.strip(), "artist": song.find(class_="a-font-primary-s").text.strip()}
            for
            song in songs]
        return tracks_and_artists


def get_track_ids(tracks):
    # Authorize spotipy, ensure the SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_ID environment variables
    # are set in order for this to work.
    spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

    # Search for the tracks via the spotify API
    track_list_response = [spotify.search(q='artist:' + track["artist"] + ' track:' + track["track"], type='track') for
                           track
                           in
                           tracks]

    track_ids = []
    for track in track_list_response:
        try:
            track_ids.append(f"spotify:track:{track['tracks']['items'][0]['id']}")
        except (IndexError, ValueError):
            pass

    return track_ids


def create_playlist_from_ids(date_selected, playlist_ids):

    # Authorize spotipy with a public modify scope
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("REDIRECT_URI"),
        scope="playlist-modify-public"
    ))

    playlist_name = f"Nostalgia {date_selected[:4]}"

    # Create a new playlist for the user.
    new_playlist = sp.user_playlist_create(user=sp.current_user()["id"],
                                           name=playlist_name,
                                           public=True,
                                           description=f"Top tracks from {date_selected}")
    # Add the tracks.
    sp.playlist_add_items(new_playlist["id"], playlist_ids)


# Ask the user what year they would like to create a playlist from.
year = input("What year you would like to travel to? Type the date in this format YYYY-MM-DD:")

# Create the billboard top 100 url by adding the year entered.
TOP_100_URL = f"https://www.billboard.com/charts/hot-100/{year}/"

# Get the tracks list.
tracks_list = get_billboard_tracks(TOP_100_URL)

# Search spotify for the track ID's.
ids = get_track_ids(tracks_list)

# Create the playlist
create_playlist_from_ids(year, ids)
