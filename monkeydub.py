import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Autenticação com Spotify API
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="TEU_CLIENT_ID_AQUI",
    client_secret="TEU_CLIENT_SECRET_AQUI",
    redirect_uri="http://127.0.0.1:8888/callback",
    scope="playlist-modify-public"
))

# Criação da playlist
user_id = sp.current_user()["id"]
playlist = sp.user_playlist_create(
    user_id,
    "Monkey Dub Sunset Vibes",
    public=True,
    description="POHB + Organic House vibes curativas 🌞"
)

# Adiciona músicas (IDs de exemplo, troca se quiser)
tracks = [
    "spotify:track:4uLU6hMCjMI75M1A2tKUQC",
    "spotify:track:1301WleyT98MSxVHPZCA6M"
]

sp.playlist_add_items(playlist["id"], tracks)

print("🔥 Playlist criada com sucesso!")
print("Link:", playlist["external_urls"]["spotify"])
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Autenticação com Spotify API
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="TEU_CLIENT_ID_AQUI",
    client_secret="TEU_CLIENT_SECRET_AQUI",
    redirect_uri="http://127.0.0.1:8888/callback",
    scope="playlist-modify-public"
))

# Criação da playlist
user_id = sp.current_user()["id"]
playlist = sp.user_playlist_create(
    user_id,
    "Monkey Dub Sunset Vibes",
    public=True,
    description="POHB + Organic House vibes curativas 🌞"
)

# Adiciona músicas (IDs de exemplo, troca se quiser)
tracks = [
    "spotify:track:4uLU6hMCjMI75M1A2tKUQC",
    "spotify:track:1301WleyT98MSxVHPZCA6M"
]

sp.playlist_add_items(playlist["id"], tracks)

print("🔥 Playlist criada com sucesso!")
print("Link:", playlist["external_urls"]["spotify"])
nano monkeydub.py

import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Autenticação com Spotify API
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="ae5f92b9784c43cfb9c7425a16123855",
    client_secret="350e1abc22af4c53acf9788f76a6dc17",
    redirect_uri="http://127.0.0.1:8888/callback",
    scope="playlist-modify-public"
))

# Criação da playlist
user_id = sp.current_user()["id"]
playlist = sp.user_playlist_create(
    user_id,
    "Monkey Dub Sunset Vibes",
    public=True,
    description="POHB + Organic House vibes curativas 🌞"
)

# Adiciona músicas (IDs de exemplo, troca se quiser)
tracks = [
    "spotify:track:4uLU6hMCjMI75M1A2tKUQC",
    "spotify:track:1301WleyT98MSxVHPZCA6M"
]

sp.playlist_add_items(playlist["id"], tracks)

print("🔥 Playlist criada com sucesso!")
print("Link:", playlist["external_urls"]["spotify"])
