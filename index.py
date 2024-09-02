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
pygame.mixer.music.play(-1)  

# Função para carregar GIFs
def carregar_gif(caminho, largura, altura):
    gif = Image.open(caminho)
    frames = []
    for frame in range(gif.n_frames):
        gif.seek(frame)
        frame_image = gif.convert("RGBA")
        frame_image = frame_image.resize((largura, altura), Image.LANCZOS)
        img_byte_arr = io.BytesIO()
        frame_image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        pygame_image = pygame.image.load(img_byte_arr)
        frames.append(pygame_image)
    return frames

# Carregar os GIFs com as dimensões especificadas
frames_inicial = carregar_gif(CAMINHO_GIF, LARGURA_GIF, ALTURA_GIF)
frames_principal = carregar_gif(CAMINHO_GIF_PRINCIPAL, LARGURA_GIF, ALTURA_GIF)

ficha_caminhos = [
    'src/imagens/1(1).png',
    'src/imagens/2(2).png',
    'src/imagens/3(3).png',
    'src/imagens/4(4).png',
    'src/imagens/5(5).png',
    'src/imagens/6(6).png',
    'src/imagens/7(7).png',
    'src/imagens/8(8).png',
    'src/imagens/9(9).png',
    'src/imagens/10(10).png'
]

# Opções de resposta para cada ficha
opcoes_fichas = [
    ["Ignorar os e-mails e continuar usando a caixa de entrada normalmente.", "Configurar filtros de spam no seu e-mail e evitar clicar em links suspeitos.", "Responder aos e-mails pedindo para que parem de enviar mensagens."],  # Opções para ficha 1
    ["Clicar no link para verificar se o site é verdadeiro.", "Ligar diretamente para a instituição \nfinanceira usando um número de telefone oficial para confirmar a solicitação.", "Responder ao e-mail pedindo mais informações."],  # Opções para ficha 2
    ["Apenas usar o navegador em modo anônimo para acessar sites bancários.", "Verificar sempre o endereço completo do site \nantes de inserir qualquer informação sensível e usar uma conexão segura.", "Confiar em links enviados por e-mail para acessar o site bancário."],  # Opções para ficha 3
    ["Ignorar os arquivos suspeitos e continuar usando o computador normalmente.", "Executar um software antivírus atualizado e considerar a \nformatação do disco rígido se necessário.", "Apagar manualmente os arquivos suspeitos e continuar trabalhando."],  # Opções para ficha 4
    ["Reiniciar todos os sistemas e esperar que o problema se resolva.", "Realizar uma auditoria completa de segurança, identificar \nvulnerabilidades e implementar patches e medidas de segurança adicionais.", "Desconectar a rede da internet e não tomar nenhuma ação adicional."],  # Opções para ficha 5
    ["Realizar uma auditoria completa de segurança para identificar a origem da invasão.", "Implementar políticas de segurança mais rígidas e treinar os \nfuncionários sobre práticas seguras.", "Monitorar continuamente os sistemas para detectar e responder a atividades suspeitas."],  # Opções para ficha 6
    ["Pedir aos funcionários para mudarem suas senhas para algo fácil de lembrar.", "Implementar políticas de senhas fortes e exigir autenticação multifator para todas as contas.", "Permitir que os funcionários usem qualquer senha, mas monitorar logins falhados."],  # Opções para ficha 7
    ["Ignorar as mensagens e continuar utilizando o aplicativo normalmente.", "Desinstalar o aplicativo suspeito, bloquear números de spam e considerar instalar um software de segurança confiável.", "Responder às mensagens de spam solicitando que parem de enviar os links."],  # Opções para ficha 8
    ["Não se preocupar, pois a transação provavelmente foi um erro do sistema e será corrigida automaticamente.", "Contactar imediatamente seu banco para bloquear o cartão, alterar suas senhas de acesso, e monitorar atentamente suas contas bancárias para atividades suspeitas.", "Tentar realizar outra compra no mesmo site para verificar se o problema se repete."],  # Opções para ficha 9
    ["Informar os funcionários afetados para que mudem suas senhas e continuar monitorando a situação.", "Isolar imediatamente os sistemas comprometidos, revogar os \nacessos das contas afetadas, e iniciar uma investigação completa para identificar e mitigar a vulnerabilidade.", "Aguardar até que o ataque termine para analisar os danos causados e depois tomar medidas corretivas."]  # Opções para ficha 10
]

# Respostas corretas para cada ficha
respostas_corretas = [
    "Configurar filtros de spam no seu e-mail e evitar clicar em links suspeitos.",  # Resposta correta para ficha 1
    "Ligar diretamente para a instituição financeira usando um número de telefone oficial para confirmar a solicitação.",  # Resposta correta para ficha 2
    "Verificar sempre o endereço completo do site antes de inserir qualquer informação sensível e usar uma conexão segura.",  # Resposta correta para ficha 3
    "Executar um software antivírus atualizado e considerar a formatação do disco rígido se necessário.",  # Resposta correta para ficha 4
    "Realizar uma auditoria completa de segurança, identificar vulnerabilidades e implementar patches e medidas de segurança adicionais.",  # Resposta correta para ficha 5
    "Realizar uma auditoria completa de segurança para identificar a origem da invasão.",  # Resposta correta para ficha 6
    "Implementar políticas de senhas fortes e exigir autenticação multifator para todas as contas.",  # Resposta correta para ficha 7
    "Desinstalar o aplicativo suspeito, bloquear números de spam e considerar instalar um software de segurança confiável.",  # Resposta correta para ficha 8
    "Contactar imediatamente seu banco para bloquear o cartão, alterar suas senhas de acesso, e monitorar atentamente suas contas bancárias para atividades suspeitas.",  # Resposta correta para ficha 9
    "Isolar imediatamente os sistemas comprometidos, revogar os acessos das contas afetadas, e iniciar uma investigação completa para identificar e mitigar a vulnerabilidade."  # Resposta correta para ficha 10
]

# Inicializar a ficha atual
indice_ficha_atual = 0

# Função para carregar e redimensionar uma imagem
def carregar_e_redimensionar_imagem(caminho, largura, altura):
    imagem = pygame.image.load(caminho).convert_alpha()
    imagem_redimensionada = pygame.transform.scale(imagem, (largura, altura))
    return imagem_redimensionada

# Carregar a imagem PNG da ficha e do livro com as dimensões especificadas
ficha_img = carregar_e_redimensionar_imagem(ficha_caminhos[indice_ficha_atual], LARGURA_FICHA, ALTURA_FICHA)
livro_imgs = [
    carregar_e_redimensionar_imagem(CAMINHO_SPRITE_LIVRO_1, LARGURA_LIVRO, ALTURA_LIVRO),
    carregar_e_redimensionar_imagem(CAMINHO_SPRITE_LIVRO_2, LARGURA_LIVRO, ALTURA_LIVRO),
    carregar_e_redimensionar_imagem(CAMINHO_SPRITE_LIVRO_3, LARGURA_LIVRO, ALTURA_LIVRO)
]
indice_livro_atual = 0

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
    if 0 <= indice_ficha_atual < len(opcoes_fichas):
        opcoes = opcoes_fichas[indice_ficha_atual]  # Carregar as opções para a ficha atual
    else:
        opcoes = []
    opcao_selecionada = None

def desenhar_ficha():
    global ficha_img, ficha_pos, opcoes, opcao_selecionada
    ficha_rect = pygame.Rect(ficha_pos[0], ficha_pos[1], ficha_img.get_width(), ficha_img.get_height())
    tela.blit(ficha_img, ficha_rect)

    fonte = pygame.font.Font(None, 25)  # Fonte intermediária

    y_offset = ficha_pos[1] + ficha_img.get_height() // 2 + 85  # Posicionar mais acima na ficha
    for i, opcao in enumerate(opcoes):
        cor = PRETO if opcao != opcao_selecionada else (255, 0, 0)  # Texto preto
        linhas = quebrar_texto(opcao, fonte, ficha_img.get_width() - 20)  # Quebrar texto em linhas
        for linha in linhas:
            texto_opcao = fonte.render(linha, True, cor)
            texto_rect = texto_opcao.get_rect(center=(ficha_pos[0] + ficha_img.get_width() // 2, y_offset))
            tela.blit(texto_opcao, texto_rect.topleft)
            y_offset += 25  # Espaçamento entre linhas
        y_offset += 25  # Espaçamento entre opções

def quebrar_texto(texto, fonte, largura_max):
    palavras = texto.split(' ')
    linhas = []
    linha_atual = []
    largura_linha_atual = 0

    for palavra in palavras:
        largura_palavra, _ = fonte.size(palavra + ' ')
        if largura_linha_atual + largura_palavra > largura_max:
            linhas.append(' '.join(linha_atual))
            linha_atual = [palavra]
            largura_linha_atual = largura_palavra
        else:
            linha_atual.append(palavra)
            largura_linha_atual += largura_palavra

    if linha_atual:
        linhas.append(' '.join(linha_atual))

    return linhas

def desenhar_livro():
    global livro_imgs, indice_livro_atual, livro_pos
    livro_img = livro_imgs[indice_livro_atual]
    livro_rect = pygame.Rect(livro_pos[0], livro_pos[1], livro_img.get_width(), livro_img.get_height())
    tela.blit(livro_img, livro_rect)

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
    pygame.quit()
    sys.exit()

def jogo_principal():
    global ficha_pos, livro_pos, ficha_exibida, livro_exibido, opcoes, opcao_selecionada
    global contador_frame_gif, atraso_frame_gif, opacidade_gif
    global indice_ficha_atual, ficha_img
    global fichas_resolvidas, respostas_certas
    global indice_livro_atual

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
                        ficha_img = carregar_e_redimensionar_imagem(ficha_caminhos[indice_ficha_atual], LARGURA_FICHA, ALTURA_FICHA)
                if evento.key == pygame.K_w:
                    livro_exibido = not livro_exibido
                if evento.key == pygame.K_e:
                    ficha_exibida = False
                    if opcao_selecionada:
                        fichas_resolvidas += 1
                        if opcao_selecionada == respostas_corretas[indice_ficha_atual]:  # Verificar se a opção selecionada é a correta
                            respostas_certas += 1
                        if fichas_resolvidas < total_fichas:
                            indice_ficha_atual = (indice_ficha_atual + 1) % len(ficha_caminhos)
                            ficha_img = carregar_e_redimensionar_imagem(ficha_caminhos[indice_ficha_atual], LARGURA_FICHA, ALTURA_FICHA)
                            carregar_ficha()
                        else:
                            tela_resultado()
                            rodando = False
                if evento.key == pygame.K_LEFT:
                    indice_livro_atual = (indice_livro_atual - 1) % len(livro_imgs)
                if evento.key == pygame.K_RIGHT:
                    indice_livro_atual = (indice_livro_atual + 1) % len(livro_imgs)

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if ficha_exibida:
                    y_offset = ficha_pos[1] + ficha_img.get_height() // 2 + 85
                    for i, opcao in enumerate(opcoes):
                        linhas = quebrar_texto(opcao, pygame.font.Font(None, 25), ficha_img.get_width() - 20)
                        for linha in linhas:
                            texto_rect = pygame.Rect(ficha_pos[0], y_offset, ficha_img.get_width(), 25)
                            if texto_rect.collidepoint(evento.pos):
                                opcao_selecionada = opcao
                            y_offset += 25
                        y_offset += 25

            arrastar_objeto(evento, ficha_img, ficha_pos)
            arrastar_objeto(evento, livro_imgs[indice_livro_atual], livro_pos)

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