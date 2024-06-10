from flask import Flask, render_template, request, jsonify
import webview
import threading

app = Flask(__name__)

channel_urls = {
    "TNT": "https://brflu.walk-tv.com/5836/tracks-v1a1/mono.m3u8",
    "GLOBO": "https://brflu.walk-tv.com/5756/tracks-v1a1/mono.m3u8",
    "ESPN": "https://cdn-3.nxplay.com.br/ESPN_4/tracks-v1a1/mono.m3u8",
    "DISCOVERY": "https://cdn-3.nxplay.com.br/DISCOVERY_CHANNEL_NX/tracks-v1a1/mono.m3u8",
    # Adicione mais URLs conforme necessário
}

def play_channel(url):
    webview.load_url(url)

def start_player(url):
    threading.Thread(target=play_channel, args=(url,)).start()

@app.route('/')
def index():
    return render_template('index.html', channels=channel_urls)

@app.route('/play', methods=['POST'])
def play():
    channel_id = request.form.get('channel_id')
    url = channel_urls.get(channel_id)
    if url:
        start_player(url)
        return jsonify(success=True, url=url)
    return jsonify(success=False), 400

if __name__ == '__main__':
    webview.create_window('Video Player', app)
    webview.start()

