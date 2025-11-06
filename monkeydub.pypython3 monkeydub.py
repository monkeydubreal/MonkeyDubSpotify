import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="TEU_CLIENT_ID",
    client_secret="TEU_CLIENT_SECRET",
    redirect_uri="http://localhost:8888/callback",
    scope="playlist-modify-public"
))

user_id = sp.current_user()["id"]
playlist = sp.user_playlist_create(user_id, "Monkey Dub Sunset Vibes", public=True, description="POHB + Organic House vibes curativas 🌞")

tracks = [
    "spotify:track:4uLU6hMCjMI75M1A2tKUQC", 
    "spotify:track:1301WleyT98MSxVHPZCA6M"
]
sp.playlist_add_items(playlist["id"], tracks)

print("🔥 Playlist criada com sucesso!")
print("Link:", playlist["external_urls"]["spotify"])

