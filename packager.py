import os
import sys

# Caminho para o seu jogo
jogo_path = "caminho/para/seu_jogo/seu_jogo.py"
# Pasta onde as imagens estão
imagens_folder = "caminho/para/seu_jogo/imagens"
# Pasta onde os áudios estão
audio_folder = "caminho/para/seu_jogo/audio"
# Pasta onde os gifs estão
gifs_folder = "caminho/para/seu_jogo/gifs"

# Comando do PyInstaller
os.system(f"pyinstaller --onefile --add-data '{imagens_folder}:imagens' --add-data '{audio_folder}:audio' --add-data '{gifs_folder}:gifs' {jogo_path}")

print("Empacotamento concluído!")
