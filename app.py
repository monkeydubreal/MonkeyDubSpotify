from flask import Flask, request, jsonify
import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="ae5f92b9784c43cfb9c7425a16123855",
    client_secret="350e1abc22af4c53acf9788f76a6dc17",
    redirect_uri="https://teuapp.onrender.com/callback",
    scope="playlist-modify-public"
))

@app.route('/')
def home():
    return "🔥 Monkey Dub Spotify API rodando!"

@app.route('/create_playlist', methods=['POST'])
def create_playlist():
    data = request.json
    vibe = data.get("vibe")
    nome = data.get("nome")
    user_id = sp.current_user()["id"]

    playlist = sp.user_playlist_create(
        user_id,
        nome,
        public=True,
        description=vibe
    )

    return jsonify({
        "status": "success",
        "playlist_url": playlist["external_urls"]["spotify"]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

@app.route('/callback')
def callback():
    sp_oauth = SpotifyOAuth(
        client_id="ae5f92b9784c43cfb9c7425a16123855",
        client_secret="TEU_CLIENT_SECRET_AQUI",
        redirect_uri="https://monkeydubspotify.onrender.com/callback",
        scope="user-read-private user-read-email playlist-read-private playlist-modify-private user-library-read user-read-currently-playing user-read-playback-state user-modify-playback-state"
    )
    code = request.args.get('code')
    if code:
        token_info = sp_oauth.get_access_token(code)
        return "✅ Token recebido com sucesso!"
    else:
        return "❌ Nenhum código recebido."


@app.route('/current_track')
def current_track():
    sp_oauth = SpotifyOAuth(
        client_id="ae5f92b9784c43cfb9c7425a16123855",
        client_secret="TEU_CLIENT_SECRET_AQUI",
        redirect_uri="https://monkeydubspotify.onrender.com/callback",
        scope="user-read-currently-playing"
    )
    token_info = sp_oauth.get_cached_token()
    if not token_info:
        return "Token expirado ou não encontrado."
    sp = spotipy.Spotify(auth=token_info["access_token"])
    track = sp.current_user_playing_track()
    if track and track['item']:
        nome = track['item']['name']
        artista = track['item']['artists'][0]['name']
        return f"🎧 Agora tocando: {nome} – {artista}"
    else:
        return "🎵 Nenhuma faixa tocando agora."


    sp_oauth = SpotifyOAuth(
        client_id="ae5f92b9784c43cfb9c7425a16123855",
        client_secret="350e1abc22af4c53acf9788f76a6dc17",
        redirect_uri="https://monkeydubspotify.onrender.com/callback",
        scope="user-read-private user-read-email playlist-read-private playlist-modify-private user-library-read user-read-currently-playing user-read-playback-state user-modify-playback-state"
    )
    code = request.args.get('code')
    if code:
        token_info = sp_oauth.get_access_token(code)
        return "✅ Token recebido com sucesso!"
    else:
        return "❌ Nenhum código recebido."

