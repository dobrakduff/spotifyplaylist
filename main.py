from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id="9ec824c528bd4efdb9a2c176f8f57998",
        client_secret="296738263b8d47d1a45b39a47530f03f",
        show_dialog=True,
        cache_path="token.txt",
        username="daipoebalu",
    )
)
user_id = sp.current_user()["id"]


playlist_date = input("Which year do you want to travel to? Type your date in this format YYYY-MM-DD ")

resource = requests.get(f"https://www.billboard.com/charts/hot-100/{playlist_date}/")
playlist_web = resource.text


soup = BeautifulSoup(playlist_web, "html.parser")
playlist = soup.select("li ul li h3")
song_name =[song.getText().strip() for song in playlist]
print(song_name)


song_uris = []
year = playlist_date.split("-")[0]
for song in song_name:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")



playlist = sp.user_playlist_create(user=user_id, name=f"{playlist_date} Billboard 100", public=False)
print(playlist)


sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)