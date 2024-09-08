import pygame
import tkinter as tk
from PIL import Image, ImageTk
from src.controlers.config import *

def fade_in(surface, opacity):
    """Aplica um efeito de fade-in a uma superfície."""
    surface_temp = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    surface_temp.fill((0, 0, 0, 0))  # Superfície transparente
    surface_temp.blit(surface, (0, 0))
    surface_temp.set_alpha(opacity)
    return surface_temp

def ficha():
    """Exibe uma imagem em um pop-up."""
    root = tk.Tk()
    root.title('Imagem Pop-up')  # Adicione um título à janela pop-up

    # Carregar a imagem (substitua 'CAMINHO_SPRITE_FICHA' pelo caminho real da sua imagem)
    imagem = ImageImageTk.open(CAMINHO_SPRITE_FICHA)
    imagem = PhotoImage(imagem)

    # Criar um rótulo com a imagem
    label = tk.Label(root, image=imagem)
    label.pack()

    # Função para fechar a janela pop-up
    def fechar_popup():
        root.destroy()

    # Define o botão de fechar
    root.protocol("WM_DELETE_WINDOW", fechar_popup)
    root.bind("<Escape>", lambda e: fechar_popup())  # Fechar com ESC

    # Executa o loop principal do tkinter
    root.mainloop()
