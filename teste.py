import vlc

try:
    instance = vlc.Instance()
    player = instance.media_player_new()
    print("VLC está funcionando corretamente.")
except Exception as e:
    print(f"Erro ao inicializar o VLC: {e}")