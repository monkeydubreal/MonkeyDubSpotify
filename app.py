from flask import Flask, request, jsonify
import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="ae5f92b9784c43cfb9c7425a16123855",
    client_secret="350e1abc22af4c53acf9788f76a6dc17",
    redirect_uri="https://monkeydubspotify.onrender.com/callback",
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


@app.route('/callback')
def callback():
    sp_oauth = SpotifyOAuth(
        client_id="ae5f92b9784c43cfb9c7425a16123855",
        client_secret="350e1abc22af4c53acf9788f76a6dc17",
        redirect_uri="https://monkeydubspotify.onrender.com/callback",
        scope="user-read-private user-read-email playlist-read-private playlist-modify-private user-library-read user-read-currently-playing user-read-playback-state user-modify-playback-state",
        cache_path=".spotifycache"
    )

    code = request.args.get('code')
    if code:
        try:
            token_info = sp_oauth.get_access_token(code, check_cache=False)
            refresh_token = token_info.get("refresh_token")
            with open(".refresh_token", "w") as f:
                f.write(refresh_token)
            return "✅ Token salvo e pronto pra renovação automática!"
        except Exception as e:
            return f"❌ Erro ao obter token: {e}"
    else:
        return "❌ Nenhum código recebido."


@app.route('/current_track')
def current_track():
    sp = get_spotify_client()

    track = sp.current_user_playing_track()
    if track and track['item']:
        nome = track['item']['name']
        artista = track['item']['artists'][0]['name']
        return f"🎧 Agora tocando: {nome} — {artista}"
    else:
        return "❌ Nenhuma faixa tocando agora."


@app.route('/vibe_track')
def vibe_track():
    sp = get_spotify_client()

    track = sp.current_user_playing_track()
    if not track or not track['item']:
        return "<h3>❌ Nenhuma faixa tocando agora!</h3>"

    nome = track['item']['name']
    artista = track['item']['artists'][0]['name']
    artista_id = track['item']['artists'][0]['id']
    artista_link = track['item']['artists'][0]['external_urls']['spotify']
    track_id = track['item']['id']
    link_spotify = track['item']['external_urls']['spotify']

    # Dados de áudio
    features = sp.audio_features([track_id])[0]
    bpm = int(features['tempo'])
    energy = features['energy']
    key_index = features['key']
    mode = features['mode']

    # Gênero do artista
    artista_info = sp.artist(artista_id)
    generos = artista_info.get('genres', [])
    genero = generos[0].title() if generos else "Indefinido"

    # Notas musicais
    notas = ["C", "C♯/D♭", "D", "D♯/E♭", "E", "F", "F♯/G♭", "G", "G♯/A♭", "A", "A♯/B♭", "B"]
    tonalidade = notas[key_index] + ("m" if mode == 0 else "")

    # Vibe da faixa
    if bpm < 115 and energy < 0.5:
        modo = "sunset"
        vibe_txt = "🌅 Vibe leve e orgânica, deixa o sol cair devagar."
    elif 115 <= bpm <= 123 and 0.5 <= energy <= 0.75:
        modo = "groove"
        vibe_txt = "💫 Groove firme, pista sorrindo, segura o flow."
    elif bpm > 123 and energy > 0.75:
        modo = "peak"
        vibe_txt = "🔥 Drop intenso, segura o grave e deixa o corpo falar."
    else:
        modo = "after"
        vibe_txt = "🌙 Clima introspectivo, deixa o som respirar."

    # Recomendações harmônicas (3)
    recs = sp.recommendations(
        seed_tracks=[track_id],
        limit=3,
        target_tempo=bpm,
        target_energy=energy,
        target_key=key_index
    )

    sugestoes_html = ""
    for i, r in enumerate(recs['tracks'][:3]):
        link_r = r['external_urls']['spotify']
        sugestoes_html += f"<li>{i+1}️⃣ <a href='{link_r}' target='_blank'>{r['name']} — {r['artists'][0]['name']}</a></li>"

    # Links externos
    beatport_url = f"https://www.beatport.com/search?q={nome.replace(' ', '+')}+{artista.replace(' ', '+')}"
    traxsource_url = f"https://www.traxsource.com/search?term={nome.replace(' ', '+')}+{artista.replace(' ', '+')}"

    # HTML estilizado
    html = f"""
    <html>
    <head>
        <title>Monkey Dub | Vibe Track</title>
        <style>
            body {{
                background-color: #0d0d0d;
                color: #f5f5f5;
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 30px;
            }}
            h1, h2 {{
                color: #00ff99;
            }}
            a {{
                color: #1DB954;
                text-decoration: none;
            }}
            a:hover {{
                text-decoration: underline;
            }}
            .info {{
                margin: 20px 0;
                font-size: 1.2em;
            }}
            ul {{
                list-style: none;
                padding: 0;
            }}
            li {{
                margin: 8px 0;
            }}
            .links a {{
                display: inline-block;
                margin: 8px;
                padding: 10px 20px;
                background: #1DB954;
                border-radius: 25px;
                color: white;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <h1>🎧 {nome}</h1>
        <h2>by {artista}</h2>
        <div class='info'>
            <p>💫 {bpm} BPM | Tom {tonalidade} | Gênero: {genero}</p>
            <p>{vibe_txt}</p>
        </div>

        <h3>🌀 Próximas na mesma onda:</h3>
        <ul>{sugestoes_html}</ul>

        <div class='links'>
            <a href='{link_spotify}' target='_blank'>🎧 Spotify</a>
            <a href='{artista_link}' target='_blank'>👤 Artista</a>
            <a href='{beatport_url}' target='_blank'>💿 Beatport</a>
            <a href='{traxsource_url}' target='_blank'>🎚️ Traxsource</a>
        </div>
    </body>
    </html>
    """

    return html



def get_spotify_client():
    sp_oauth = SpotifyOAuth(
        client_id="ae5f92b9784c43cfb9c7425a16123855",
        client_secret="350e1abc22af4c53acf9788f76a6dc17",
        redirect_uri="https://monkeydubspotify.onrender.com/callback",
        scope="user-read-private user-read-email playlist-read-private playlist-modify-private user-library-read user-read-currently-playing user-read-playback-state user-modify-playback-state",
        cache_path=".spotifycache"
    )

    token_info = None

    try:
        # tenta renovar usando o refresh_token salvo
        with open(".refresh_token", "r") as f:
            refresh_token = f.read().strip()
            token_info = sp_oauth.refresh_access_token(refresh_token)
    except FileNotFoundError:
        print("⚠️ Nenhum refresh_token encontrado. É preciso logar de novo.")
    except Exception as e:
        print(f"⚠️ Erro ao renovar token: {e}")

    # se não conseguir, tenta pegar do cache
    if not token_info:
        token_info = sp_oauth.get_cached_token()

    # se ainda não tiver token, avisa
    if not token_info:
        raise Exception("🚫 Nenhum token válido encontrado. Acesse /callback primeiro!")

    return spotipy.Spotify(auth=token_info["access_token"])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
