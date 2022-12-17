from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth


URL = "https://www.billboard.com/charts/hot-100/"
CLIENT_ID = "075a4b9124194a49ab0a91579b222297"
CLIENT_SECRET = "7766363eaa6e408d9c2e176b35476b58"
REDIRECT_URI = "http://example.com"
SPOTIFY_ENDPOINT = "https://api.spotify.com/v1/users/{user_id}/playlists"


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=REDIRECT_URI,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
date = input("Which year do you want to travel to? Type the data in this format YYYY-MM-DD: ")
response = requests.get(URL + date)
billboard_site = response.text
soup = BeautifulSoup(billboard_site, "html.parser")

user_id = sp.current_user()["id"]

song_names_spans = soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")
song_names = [song.getText() for song in song_names_spans]

song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in spotify. Skipped.")

playlist = sp.user_playlist_create(
    user=user_id,
    name=f"{date} Billboard 100",
    public=False,
    collaborative=False,
    description="Using music as a time machine. by Jeffrey Jeremiah"
)

PLAYLIST_ID = playlist["id"]

sp.playlist_add_items(playlist_id=PLAYLIST_ID, items=song_uris)
