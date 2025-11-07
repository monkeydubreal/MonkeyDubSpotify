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
        return "❌ Nenhuma faixa tocando agora!"

    nome = track['item']['name']
    artista = track['item']['artists'][0]['name']
    track_id = track['item']['id']

    features = sp.audio_features([track_id])[0]
    bpm = int(features['tempo'])
    energy = features['energy']
    key_index = features['key']
    mode = features['mode']

    # 🎵 Tonalidade (key + modo)
    notas = ["C", "C♯/D♭", "D", "D♯/E♭", "E", "F", "F♯/G♭", "G", "G♯/A♭", "A", "A♯/B♭", "B"]
    tonalidade = notas[key_index] + ("m" if mode == 0 else "")

    # 🌅 Define o "clima" da faixa
    if bpm < 115 and energy < 0.5:
        vibe = "☀️ Sunset — vibe leve e orgânica, mixa com tons suaves."
    elif 115 <= bpm <= 123 and 0.5 <= energy <= 0.75:
        vibe = "💃 Groove — pista firme, fluindo suave."
    elif bpm > 123 and energy > 0.75:
        vibe = "🔥 Peak time — energia alta, hora do drop pesado!"
    else:
        vibe = "🌙 After — introspectivo, vibe noturna e densa."

    # 🎯 Sugestões compatíveis
    recs = sp.recommendations(
        seed_tracks=[track_id],
        limit=3,
        target_tempo=bpm,
        target_energy=energy,
        target_key=key_index
    )

    if recs['tracks']:
        sugestoes = []
        for i, rec in enumerate(recs['tracks'][:3]):
            nome_rec = rec['name']
            artista_rec = rec['artists'][0]['name']
            link = rec['external_urls']['spotify']
            sugestoes.append(f"{i+1}. [{nome_rec} — {artista_rec}]({link})")
        sugestoes_txt = "\n".join(sugestoes)
    else:
        sugestoes_txt = "⚡ Nenhuma sugestão perfeita no momento."

    return f"""
    🎧 Tocando agora: <b>{nome}</b> — {artista}<br>
    💫 <b>{bpm} BPM</b> | Tom <b>{tonalidade}</b><br><br>
    {vibe}<br><br>
    🎯 <b>Sugestões Monkey Dub:</b><br>
    {sugestoes_txt}
    """



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
