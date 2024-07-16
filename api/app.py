from flask import Flask, render_template, request, jsonify
import vlc
import time
import threading

app = Flask(__name__)

# Variável global para armazenar o tempo de início da exibição da programação
start_time = None
player = None
elemento= False



# Mapeamento de URLs dos canais (exemplo com a URL fornecida)
channel_urls = {
    "40": "http://selpro1348.procergs.com.br:1935/tve/stve/playlist.m3u",
    
}

# Função para reproduzir um canal usando VLC
def play_channel(url):
    global start_time, player
    try:
        print("Inicializando VLC...")
        instance = vlc.Instance("--network-caching=2000", "--file-caching=2000", "--live-caching=2000")
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
    time.sleep(8)
    elemento= True
    return render_template('index.html', channels=channel_urls,elemento=elemento)

# Rota para iniciar a reprodução
@app.route('/play', methods=['POST'])
def play():
    channel_id = request.form.get('channel_id')
    url = channel_urls.get(channel_id)
    if url:
        print(f"Iniciando canal {channel_id} com URL {url}")
        threading.Thread(target=delayed_start, args=(url, 5)).start()  # Iniciando com delay de 5 segundos
        return jsonify(success=True, url=url)
    print(f"Falha ao iniciar o canal {channel_id}: URL não encontrada")
    return jsonify(success=False), 400

# Função para iniciar a reprodução com atraso
def delayed_start(url, delay):
    time.sleep(delay)
    monitor_player(url)

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
