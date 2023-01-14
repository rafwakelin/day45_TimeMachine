from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import config

scope = "playlist-modify-public"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=config.SPOTIPY_CLIENT_ID,
                                               client_secret=config.SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=config.SPOTIPY_REDIRECT_URI,
                                               scope=scope,
                                               show_dialog=True,
                                               cache_path="token.txt"))
user_id = sp.current_user()["id"]

back_to = input("Which date would you like to travel back to in YYY-MM-DD format? ")

url = f"https://www.billboard.com/charts/hot-100/{back_to}/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
music_list = soup.select(selector='li #title-of-a-story')
song_names = [_.getText().strip() for _ in music_list]

song_uris = []
year = back_to.split("-")[0]

for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")

    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{back_to} Billboard 100", public=True, collaborative=False,
                                   description=f"100 top Billboard chart on {back_to}")
print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
