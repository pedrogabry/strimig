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
    "40": "https://brflu.walk-tv.com/5814/tracks-v1a1/mono.m3u8",
    "41": "https://brflu.walk-tv.com/5815/tracks-v1a1/mono.m3u8",
    "42": "https://brflu.walk-tv.com/5816/tracks-v1a1/mono.m3u8",
    "Megapix": "https://brflu.walk-tv.com/5822/tracks-v1a1/mono.m3u8",
    "Telecine action": "https://brflu.walk-tv.com/5875/tracks-v1a1/mono.m3u8",
    "Telecine Pipoca": "https://brflu.walk-tv.com/5877/tracks-v1a1/mono.m3u8",
    "star shanel": "https://brflu.walk-tv.com/5889/tracks-v1a1/mono.m3u8",
    "Telecine Premium": "https://brflu.walk-tv.com/5879/tracks-v1a1/mono.m3u8",
    "Telecine touch": "https://brflu.walk-tv.com/5880/tracks-v1a1/mono.m3u8",
    "Telecine Cult": "https://brflu.walk-tv.com/5899/tracks-v1a1/mono.m3u8",
    "Telecine Fun": "https://brflu.walk-tv.com/5901/tracks-v1a1/mono.m3u8",
    "TLC": "https://brflu.walk-tv.com/5902/tracks-v1a1/mono.m3u8",
    "TNT": "https://brflu.walk-tv.com/5904/tracks-v1a1/mono.m3u8",
    "espn": "https://brflu.walk-tv.com/5912/tracks-v1a1/mono.m3u8",
    "Premiere1": "https://brflu.walk-tv.com/5914/tracks-v1a1/mono.m3u8",
    "Premiere": "https://brflu.walk-tv.com/5915/tracks-v1a1/mono.m3u8",
    "0": "https://brflu.walk-tv.com/5724/tracks-v1a1/mono.m3u8",
    "1": "https://brflu.walk-tv.com/5729/tracks-v1a1/mono.m3u8",
    "2": "https://brflu.walk-tv.com/5736/tracks-v1a1/mono.m3u8",
    "3": "https://brflu.walk-tv.com/5738/tracks-v1a1/mono.m3u8",
    "4": "https://brflu.walk-tv.com/5740/tracks-v1a1/mono.m3u8",
    "5": "https://brflu.walk-tv.com/5752/tracks-v1a1/mono.m3u8",
    "6": "https://brflu.walk-tv.com/5754/tracks-v1a1/mono.m3u8",
    "7": "https://brflu.walk-tv.com/5755/tracks-v1a1/mono.m3u8",
    "8": "https://brflu.walk-tv.com/5756/tracks-v1a1/mono.m3u8",
    "9": "https://brflu.walk-tv.com/5758/tracks-v1a1/mono.m3u8",
    "10": "https://brflu.walk-tv.com/5759/tracks-v1a1/mono.m3u8",
    "11": "https://brflu.walk-tv.com/5763/tracks-v1a1/mono.m3u8",
    "12": "https://brflu.walk-tv.com/5766/tracks-v1a1/mono.m3u8",

    "22": "https://brflu.walk-tv.com/5787/tracks-v1a1/mono.m3u8",
    "23": "https://brflu.walk-tv.com/5789/tracks-v1a1/mono.m3u8",

    "25": "https://brflu.walk-tv.com/5791/tracks-v1a1/mono.m3u8",
    "26": "https://brflu.walk-tv.com/5792/tracks-v1a1/mono.m3u8",

    "28": "https://brflu.walk-tv.com/5794/tracks-v1a1/mono.m3u8",
    "29": "https://brflu.walk-tv.com/5796/tracks-v1a1/mono.m3u8",
    "30": "https://brflu.walk-tv.com/5799/tracks-v1a1/mono.m3u8",

    "32": "https://brflu.walk-tv.com/5804/tracks-v1a1/mono.m3u8",
    "33": "https://brflu.walk-tv.com/5805/tracks-v1a1/mono.m3u8",
    "34": "https://brflu.walk-tv.com/5806/tracks-v1a1/mono.m3u8",
    "35": "https://brflu.walk-tv.com/5807/tracks-v1a1/mono.m3u8",
    
    "44": "https://brflu.walk-tv.com/5825/tracks-v1a1/mono.m3u8",
    "45": "https://brflu.walk-tv.com/5826/tracks-v1a1/mono.m3u8",
    "46": "https://brflu.walk-tv.com/5827/tracks-v1a1/mono.m3u8",
    "47": "https://brflu.walk-tv.com/5829/tracks-v1a1/mono.m3u8",
    "48": "https://brflu.walk-tv.com/5835/tracks-v1a1/mono.m3u8",
    "49": "https://brflu.walk-tv.com/5836/tracks-v1a1/mono.m3u8",
    "50": "https://brflu.walk-tv.com/5837/tracks-v1a1/mono.m3u8",
    "51": "https://brflu.walk-tv.com/5838/tracks-v1a1/mono.m3u8",
    "52": "https://brflu.walk-tv.com/5847/tracks-v1a1/mono.m3u8",
    "53": "https://brflu.walk-tv.com/5850/tracks-v1a1/mono.m3u8",
    "54": "https://brflu.walk-tv.com/5851/tracks-v1a1/mono.m3u8",
    "55": "https://brflu.walk-tv.com/5853/tracks-v1a1/mono.m3u8",
    "56": "https://brflu.walk-tv.com/5855/tracks-v1a1/mono.m3u8",
    "57": "https://brflu.walk-tv.com/5857/tracks-v1a1/mono.m3u8",
    "58": "https://brflu.walk-tv.com/5859/tracks-v1a1/mono.m3u8",
    "59": "https://brflu.walk-tv.com/5861/tracks-v1a1/mono.m3u8",
    "60": "https://brflu.walk-tv.com/5865/tracks-v1a1/mono.m3u8",
    "61": "https://brflu.walk-tv.com/5867/tracks-v1a1/mono.m3u8",
    "66": "https://brflu.walk-tv.com/5882/tracks-v1a1/mono.m3u8",
    "67": "https://brflu.walk-tv.com/5886/tracks-v1a1/mono.m3u8",
    "69": "https://brflu.walk-tv.com/5891/tracks-v1a1/mono.m3u8",
    "70": "https://brflu.walk-tv.com/5893/tracks-v1a1/mono.m3u8",
    "71": "https://brflu.walk-tv.com/5895/tracks-v1a1/mono.m3u8",
    "72": "https://brflu.walk-tv.com/5897/tracks-v1a1/mono.m3u8",
    "77": "https://brflu.walk-tv.com/5907/tracks-v1a1/mono.m3u8",
    "78": "https://brflu.walk-tv.com/5910/tracks-v1a1/mono.m3u8",
    "82": "https://brflu.walk-tv.com/5916/tracks-v1a1/mono.m3u8",
    "83": "https://brflu.walk-tv.com/5918/tracks-v1a1/mono.m3u8",
    "84": "https://brflu.walk-tv.com/5920/tracks-v1a1/mono.m3u8",
    "85": "https://brflu.walk-tv.com/5921/tracks-v1a1/mono.m3u8",
    "86": "https://brflu.walk-tv.com/5922/tracks-v1a1/mono.m3u8",
    "87": "https://brflu.walk-tv.com/5924/tracks-v1a1/mono.m3u8",
    "88": "https://brflu.walk-tv.com/5928/tracks-v1a1/mono.m3u8",
    "89": "https://brflu.walk-tv.com/5930/tracks-v1a1/mono.m3u8",
    "90": "https://brflu.walk-tv.com/5931/tracks-v1a1/mono.m3u8",
    "91": "https://brflu.walk-tv.com/5932/tracks-v1a1/mono.m3u8",
    "92": "https://brflu.walk-tv.com/6431/tracks-v1a1/mono.m3u8",
    "93": "https://brflu.walk-tv.com/6586/tracks-v1a1/mono.m3u8",

    "premiere": "http://45.235.0.78/PREMIERECLUBES-HD/index.m3u8"
    
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
    return render_template('index.html', channels=channel_urls)

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
