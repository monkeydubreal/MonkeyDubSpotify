from flask import Flask, request, jsonify
import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)

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
        with open(".refresh_token", "r") as f:
            refresh_token = f.read().strip()
            token_info = sp_oauth.refresh_access_token(refresh_token)
    except Exception:
        token_info = sp_oauth.get_cached_token()

    if not token_info:
        raise Exception("🚫 Nenhum token válido encontrado. Acesse /callback primeiro!")

    return spotipy.Spotify(auth=token_info["access_token"])


@app.route('/')
def home():
    return "🔥 Monkey Dub Spotify API rodando!"


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
        token_info = sp_oauth.get_access_token(code, check_cache=False)
        refresh_token = token_info.get("refresh_token")
        if refresh_token:
            with open(".refresh_token", "w") as f:
                f.write(refresh_token)
        return "✅ Token salvo e pronto pra renovação automática!"
    else:
        return "❌ Nenhum código recebido."


@app.route('/vibe_track')
def vibe_track():
    try:
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

        features = sp.audio_features([track_id])[0]
        if not features:
            return "<h3>⚠️ Dados de áudio não disponíveis para esta faixa.</h3>"

        bpm = int(features.get('tempo', 0))
        energy = features.get('energy', 0)
        key_index = features.get('key', 0)
        mode = features.get('mode', 1)

        artista_info = sp.artist(artista_id)
        generos = artista_info.get('genres', [])
        genero = generos[0].title() if generos else "Indefinido"

        notas = ["C", "C♯/D♭", "D", "D♯/E♭", "E", "F", "F♯/G♭", "G", "G♯/A♭", "A", "A♯/B♭", "B"]
        tonalidade = notas[key_index] + ("m" if mode == 0 else "")

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

        recs = sp.recommendations(seed_tracks=[track_id], limit=3,
                                  target_tempo=bpm, target_energy=energy, target_key=key_index)

        sugestoes_html = ""
        for i, r in enumerate(recs.get('tracks', [])[:3]):
            link_r = r['external_urls']['spotify']
            sugestoes_html += f"<li>{i+1}️⃣ <a href='{link_r}' target='_blank'>{r['name']} — {r['artists'][0]['name']}</a></li>"

        beatport_url = f"https://www.beatport.com/search?q={nome.replace(' ', '+')}+{artista.replace(' ', '+')}"
        traxsource_url = f"https://www.traxsource.com/search?term={nome.replace(' ', '+')}+{artista.replace(' ', '+')}"

        html = f"""
        <html>
        <head>
            <title>Monkey Dub | Vibe Track</title>
            <style>
                body {{
                    background-color: #0d0d0d;
                    color: #f5f5
                    
                        return html


# 🔹 Fim do arquivo (fora de qualquer função)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

