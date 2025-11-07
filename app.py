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

    )
    code = request.args.get('code')

    if code:
        try:
            token_info = sp_oauth.get_access_token(code, check_cache=False)
            return "✅ Token recebido com sucesso!"
        except Exception as e:
            return f"❌ Erro ao obter token: {e}"
    else:
        return "❌ Nenhum código recebido."



@app.route('/current_track')
def current_track():
    sp = get_spotify_client()  # usa o token automaticamente renovado

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
        return "❌ Nenhuma faixa tocando agora, bro. Solta o play e me chama de volta!"

    nome = track['item']['name']
    artista = track['item']['artists'][0]['name']
    track_id = track['item']['id']

    # pega os dados de áudio da faixa atual
    features = sp.audio_features([track_id])[0]
    bpm = int(features['tempo'])
    energy = features['energy']
    key_index = features['key']
    mode = features['mode']

    # mapeia tonalidades (0–11 → notas)
    notas = ["C", "C♯/D♭", "D", "D♯/E♭", "E", "F", "F♯/G♭", "G", "G♯/A♭", "A", "A♯/B♭", "B"]
    tonalidade = notas[key_index] + ("m" if mode == 0 else "")

    # define o modo de energia
    if bpm < 115 and energy < 0.5:
        modo = "sunset"
    elif 115 <= bpm <= 123 and 0.5 <= energy <= 0.75:
        modo = "groove"
    elif bpm > 123 and energy > 0.75:
        modo = "peak"
    else:
        modo = "after"

    # busca faixas similares com base em BPM, energia e tonalidade
    recommendations = sp.recommendations(
        seed_tracks=[track_id],
        limit=5,
        target_tempo=bpm,
        target_energy=energy,
        target_key=key_index
    )

    # escolhe a melhor sugestão (mais próxima de BPM/energia)
    if recommendations['tracks']:
        next_track = recommendations['tracks'][0]
        next_name = next_track['name']
        next_artist = next_track['artists'][0]['name']
        next_bpm = sp.audio_features([next_track['id']])[0]['tempo']
        sugestao = f"🎯 Próxima faixa ideal: {next_name} — {next_artist} ({int(next_bpm)} BPM)"
    else:
        sugestao = "⚡ Não encontrei sugestão perfeita agora, mas o groove continua contigo!"

    # mensagem por energia / modo
    if modo == "sunset":
        vibe = f"🌅 {bpm} BPM em {tonalidade} — vibe leve e orgânica. Mixa com tons vizinhos ({notas[(key_index+1)%12]} ou {notas[(key_index+11)%12]})."
    elif modo == "groove":
        vibe = f"💫 {bpm} BPM em {tonalidade} — groove firme, pista sorrindo. Mantém dentro da mesma key ou sobe meio tom se quiser abrir."
    elif modo == "peak":
        vibe = f"🔥 {bpm} BPM em {tonalidade} — energia alta! Ideal pra drop pesado, mantém tensão harmônica e segura o grave."
    else:
        vibe = f"🌙 {bpm} BPM em {tonalidade} — after feeling... introspectivo e profundo. Deixa o som respirar."

    # resposta final estilo Monkey Dub 🎧
    return f"""
    🎧 Bro, olha o som:
    👉 {nome} — {artista}

    {vibe}
    {sugestao}
    """




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


def get_spotify_client():
    sp_oauth = SpotifyOAuth(
        client_id="ae5f92b9784c43cfb9c7425a16123855",
        client_secret="350e1abc22af4c53acf97887f6a6dc17",
        redirect_uri="https://monkeydubspotify.onrender.com/callback",
        scope="user-read-currently-playing",
        cache_path=".spotifycache"
    )

    try:
        with open(".refresh_token", "r") as f:
            refresh_token = f.read().strip()
            token_info = sp_oauth.refresh_access_token(refresh_token)
    except Exception:
        token_info = sp_oauth.get_cached_token()

    return spotipy.Spotify(auth=token_info["access_token"])



