import pygame
import pygame_gui
from pygame.locals import *
from PIL import Image
import io
import sys
from src.controlers.buttons import Button
from src.controlers.utils import *
from src.controlers.config import *

pygame.init()
pygame.mixer.init()

# Configurações iniciais da tela
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption('Menu Principal')

# Carregar música de fundo
pygame.mixer.music.load(CAMINHO_MUSICA)
pygame.mixer.music.play(-1)  # -1 faz com que a música toque em loop

# Função para carregar GIFs
def carregar_gif(caminho):
    gif = Image.open(caminho)
    frames = []
    for frame in range(gif.n_frames):
        gif.seek(frame)
        frame_image = gif.convert("RGBA")
        img_byte_arr = io.BytesIO()
        frame_image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        pygame_image = pygame.image.load(img_byte_arr)
        frames.append(pygame_image)
    return frames

# Carregar os GIFs
frames_inicial = carregar_gif(CAMINHO_GIF)
frames_principal = carregar_gif(CAMINHO_GIF_PRINCIPAL)

# Caminhos das fichas
ficha_caminhos = [
    'src/imagens/1.png',
    'src/imagens/3.png',
    'src/imagens/4.png',
    'src/imagens/5.png',
    'src/imagens/6.png',
    'src/imagens/7.png'
]

# Opções de resposta para cada ficha
opcoes_fichas = [
    ["Ignorar os e-mails e continuar usando a caixa de entrada normalmente.", "Responder aos e-mails pedindo para que parem de enviar mensagens.", "Configurar filtros de spam no seu e-mail e evitar clicar em links suspeitos"],  # Opções para ficha 1
    ["Ignorar os arquivos suspeitos e continuar usando o computador normalmente.", "Executar um software antivírus atualizado e considerar a formatação do disco rígido se necessário.", "Apagar manualmente os arquivos suspeitos e continuar trabalhando."],  # Opções para ficha 2
    ["Clicar no link para verificar se o site é verdadeiro.", "Responder ao e-mail pedindo mais informações.", "Ligar diretamente para a instituição financeira usando um número de telefone oficial para confirmar a solicitação. "],  # Opções para ficha 3
    ["Apenas usar o navegador em modo anônimo para acessar sites bancários.", "Verificar sempre o endereço completo do site antes de inserir qualquer informação sensível e usar uma conexão segura.", "Confiar em links enviados por e-mail para acessar o site bancário."],  # Opções para ficha 4
    ["Permitir que os funcionários usem qualquer senha, mas monitorar logins falhados.", "Pedir aos funcionários para mudarem suas senhas para algo fácil de lembrar.", "Implementar políticas de senhas fortes e exigir autenticação multifator para todas as contas."],  # Opções para ficha 5
    ["Realizar uma auditoria completa de segurança, identificar vulnerabilidades e implementar patches e medidas de segurança adicionais.", "Reiniciar todos os sistemas e esperar que o problema se resolva.", "Desconectar a rede da internet e não tomar nenhuma ação adicional."],  # Opções para ficha 6
]

# Inicializar a ficha atual
indice_ficha_atual = 0





# Carregar a imagem PNG da ficha e do livro
ficha_img = pygame.image.load(ficha_caminhos[indice_ficha_atual]).convert_alpha()
livro_img = pygame.image.load(CAMINHO_SPRITE_LIVRO).convert_alpha()

# Inicializar variáveis para o arrasto
arrastando_objeto = None
ficha_pos = [100, 100]  # Posição inicial da ficha
livro_pos = [200, 200]  # Posição inicial do livro
ficha_exibida = False
livro_exibido = False
opcoes = []
opcao_selecionada = None

# Inicializar outras variáveis globais
contador_frame_gif = 0
atraso_frame_gif = 5
opacidade_gif = 255  # Valor máximo de opacidade
pontos = 0
total_fichas = len(ficha_caminhos)
fichas_resolvidas = 0
respostas_certas = 0

# Função para criar o efeito de fade-in
def fade_in(surface, opacity):
    temp_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    temp_surface.blit(surface, (0, 0))
    temp_surface.set_alpha(opacity)
    return temp_surface

# Criação dos botões
botao_iniciar = Button(text="INICIAR", pos=(LARGURA_TELA // 2, ALTURA_TELA // 2 - 50), font=30, bg="gray", fg=BRANCO)
botao_controles = Button(text="CONTROLES", pos=(LARGURA_TELA // 2, ALTURA_TELA // 2 + 50), font=30, bg="gray", fg=BRANCO)
botao_sair = Button(text="SAIR", pos=(LARGURA_TELA // 2, ALTURA_TELA // 2 + 150), font=30, bg="gray", fg=BRANCO)

def carregar_ficha():
    global opcoes, opcao_selecionada
    opcoes = opcoes_fichas[indice_ficha_atual]  # Carregar as opções para a ficha atual
    opcao_selecionada = None

def desenhar_ficha():
    global ficha_img, ficha_pos, opcoes, opcao_selecionada
    ficha_rect = pygame.Rect(ficha_pos[0], ficha_pos[1], ficha_img.get_width(), ficha_img.get_height())
    tela.blit(ficha_img, ficha_rect)

    fonte = pygame.font.Font(None, 25)  # Fonte menor

    y_offset = ficha_pos[1] + ficha_img.get_height() // 2 + 30  # Posicionar mais abaixo na ficha
    for i, opcao in enumerate(opcoes):
        cor = PRETO if opcao != opcao_selecionada else (255, 0, 0)  # Texto preto
        texto_opcao = fonte.render(opcao, True, cor)
        texto_rect = texto_opcao.get_rect(center=(ficha_pos[0] + ficha_img.get_width() // 2, y_offset))
        tela.blit(texto_opcao, texto_rect.topleft)
        if texto_rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:  # Botão esquerdo do mouse
                opcao_selecionada = opcao
        y_offset += 40

def desenhar_livro():
    global livro_img, livro_pos
    livro_rect = pygame.Rect(livro_pos[0], livro_pos[1], livro_img.get_width(), livro_img.get_height())
    tela.blit(livro_img, livro_rect)


# Função para redimensionar a ficha
def redimensionar_ficha(imagem, escala=1.5):
    largura = int(imagem.get_width() * escala)
    altura = int(imagem.get_height() * escala)
    return pygame.transform.scale(imagem, (largura, altura))


# Carregar a imagem PNG da ficha e redimensionar

ficha_img = redimensionar_ficha(pygame.image.load(ficha_caminhos[indice_ficha_atual]).convert_alpha())

def arrastar_objeto(evento, objeto_img, objeto_pos):
    global arrastando_objeto, offset_x, offset_y

    objeto_rect = pygame.Rect(objeto_pos[0], objeto_pos[1], objeto_img.get_width(), objeto_img.get_height())

    if evento.type == pygame.MOUSEBUTTONDOWN:
        if objeto_rect.collidepoint(evento.pos):
            arrastando_objeto = objeto_img
            mouse_x, mouse_y = evento.pos
            offset_x, offset_y = objeto_pos[0] - mouse_x, objeto_pos[1] - mouse_y

    elif evento.type == pygame.MOUSEBUTTONUP:
        arrastando_objeto = None

    elif evento.type == pygame.MOUSEMOTION:
        if arrastando_objeto == objeto_img:
            mouse_x, mouse_y = evento.pos
            objeto_pos[0] = mouse_x + offset_x
            objeto_pos[1] = mouse_y + offset_y

def menu_principal():
    global opacidade_gif
    global contador_frame_gif, atraso_frame_gif

    rodando = True
    while rodando:
        tela.fill(PRETO)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_iniciar.is_clicked(evento.pos):
                    rodando = False
                    jogo_principal()
                if botao_controles.is_clicked(evento.pos):
                    pass
                if botao_sair.is_clicked(evento.pos):
                    pygame.quit()
                    sys.exit()

        contador_frame_gif += 1
        if contador_frame_gif >= atraso_frame_gif:
            contador_frame_gif = 0

        tela.blit(fade_in(frames_inicial[contador_frame_gif], opacidade_gif), (0, 0))
        botao_iniciar.draw(tela)
        botao_controles.draw(tela)
        botao_sair.draw(tela)

        pygame.display.flip()
        pygame.time.Clock().tick(60)

def tela_resultado():
    global pontos, respostas_certas, total_fichas
    tela.fill(PRETO)
    fonte = pygame.font.Font(None, 50)
    resultado_texto = f"Você acertou {respostas_certas} de {total_fichas} perguntas!"
    resultado_surf = fonte.render(resultado_texto, True, BRANCO)
    resultado_rect = resultado_surf.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2))
    tela.blit(resultado_surf, resultado_rect.topleft)
    pygame.display.flip()
    pygame.time.wait(5000)

def jogo_principal():
    global ficha_pos, livro_pos, ficha_exibida, livro_exibido, opcoes, opcao_selecionada
    global contador_frame_gif, atraso_frame_gif, opacidade_gif
    global indice_ficha_atual, ficha_img
    global fichas_resolvidas, respostas_certas

    rodando = True
    carregar_ficha()

    while rodando:
        tela.fill(PRETO)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_q:
                    ficha_exibida = not ficha_exibida
                    if ficha_exibida:
                        ficha_img = pygame.image.load(ficha_caminhos[indice_ficha_atual]).convert_alpha()
                if evento.key == pygame.K_w:
                    livro_exibido = not livro_exibido
                if evento.key == pygame.K_e:
                    ficha_exibida = False
                    if opcao_selecionada:
                        # Atualizar o sistema de pontos e lógica de respostas
                        fichas_resolvidas += 1
                        if opcao_selecionada == "Opção correta":  # Verificar se a opção selecionada é a correta
                            respostas_certas += 1
                        if fichas_resolvidas < total_fichas:
                            indice_ficha_atual = (indice_ficha_atual + 1) % len(ficha_caminhos)
                            ficha_img = pygame.image.load(ficha_caminhos[indice_ficha_atual]).convert_alpha()
                            carregar_ficha()
                        else:
                            tela_resultado()
                            rodando = False

            arrastar_objeto(evento, ficha_img, ficha_pos)
            arrastar_objeto(evento, livro_img, livro_pos)

        contador_frame_gif += 1
        if contador_frame_gif >= atraso_frame_gif:
            contador_frame_gif = 0

        tela.blit(fade_in(frames_principal[contador_frame_gif], opacidade_gif), (0, 0))

        if ficha_exibida:
            desenhar_ficha()
        if livro_exibido:
            desenhar_livro()

        pygame.display.flip()
        pygame.time.Clock().tick(60)

menu_principal()
