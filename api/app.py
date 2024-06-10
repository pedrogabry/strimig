from flask import Flask, render_template, request, jsonify
import vlc
import time
import threading

app = Flask(__name__)

# Variável global para armazenar o tempo de início da exibição da programação
start_time = None
player = None

# Mapeamento de URLs dos canais (exemplo com a URL fornecida)
channel_urls = {
    "premier":"http://evpp.mm.uol.com.br/ne10/ne10.smil/playlist.m3u8?EDSONSOUSALIST",
    "paramont":"https://watch.vcdn.in/paramount/index.m3u8",
    "TNT Series":"https://watch.vcdn.in/tntseries/index.m3u8",
    "Warner Channel":"https://watch.vcdn.in/warnerchannel/index.m3u8",
    "Telecine Pipoca":"https://watch.vcdn.in/telecinepipoca/index.m3u8",
    "Telecine Fun":"https://watch.vcdn.in/telecinefun/index.m3u8",
    "TNT":"https://watch.vcdn.in/tnt/index.m3u8",
    "Telecine action": "https://watch.vcdn.in/telecineaction/index.m3u8",
    "2":"https://video01.logicahost.com.br/redefamiliaa/redefamiliaa/chunklist_w1049597052.m3u8",
    "Telecine Premium":"https://watch.vcdn.in/telecinepremium/index.m3u8",
    "GLOBO": "https://brflu.walk-tv.com/5756/tracks-v1a1/mono.m3u8",
    "ESPN": "https://cdn-3.nxplay.com.br/ESPN_4/tracks-v1a1/mono.m3u8",
    "DISCOVERY": "https://cdn-3.nxplay.com.br/DISCOVERY_CHANNEL_NX/tracks-v1a1/mono.m3u8",
    # Adicione mais URLs conforme necessário
}

# Função para reproduzir um canal usando VLC
def play_channel(url):
    global start_time, player
    try:
        print("Inicializando VLC...")
        instance = vlc.Instance("--network-caching=1000", "--file-caching=1000", "--live-caching=1000")
        player = instance.media_player_new()
        media = instance.media_new(url)
        player.set_media(media)
        player.play()
        print("Canal iniciado.")
        start_time = time.time()
        return player
    except Exception as e:
        print(f"Erro ao tentar reproduzir o canal: {e}")
        return None

# Função para monitorar a reprodução e evitar travamentos
def monitor_player(url):
    global start_time, player
    try:
        while True:
            if player:
                state = player.get_state()
                if state in [vlc.State.Ended, vlc.State.Error]:
                    print("Reprodução terminou ou ocorreu um erro. Tentando reiniciar...")
                    player.stop()
                    start_time = None
                    time.sleep(1)
                    player = play_channel(url)
            time.sleep(1)
    except KeyboardInterrupt:
        if player:
            player.stop()
        start_time = None
        print("Reprodução encerrada pelo usuário.")

# Rota para a página principal
@app.route('/')
def index():
    return render_template('index.html', channels=channel_urls)

# Rota para iniciar a reprodução
@app.route('/play', methods=['POST'])
def play():
    channel_id = request.form.get('channel_id')
    url = channel_urls.get(channel_id)
    if url:
        print(f"Iniciando canal {channel_id} com URL {url}")
        threading.Thread(target=monitor_player, args=(url,)).start()
        return jsonify(success=True, url=url)
    print(f"Falha ao iniciar o canal {channel_id}: URL não encontrada")
    return jsonify(success=False), 400

# Rota para obter o tempo de exibição
@app.route('/time')
def get_time():
    global start_time
    if start_time:
        elapsed_time = time.time() - start_time
        return jsonify(time=elapsed_time)
    return jsonify(time=0)

if __name__ == '__main__':
    app.run(debug=True)
