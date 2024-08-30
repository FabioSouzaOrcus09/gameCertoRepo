import pygame #type: ignore

class Button:
    def __init__(self, text, pos, font, bg, fg):
        self.font = pygame.font.Font(None, font)
        self.text = text
        self.bg = bg
        self.fg = fg
        self.rect = pygame.Rect(pos, (100, 50))  # Ajuste o tamanho conforme necessário
        self.clicked = False

    def draw(self, surface):
        # Desenha o botão
        pygame.draw.rect(surface, self.bg, self.rect)
        text_surface = self.font.render(self.text, True, self.fg)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        # Verifica se o botão foi clicado
        if self.rect.collidepoint(pos):
            if not self.clicked:
                self.clicked = True
                return True
        else:
            self.clicked = False
        return False
