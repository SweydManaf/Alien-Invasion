import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Uma classe que representa um unico alienigena da frota."""

    def __init__(self, ai_settings, screen):
        """Inicializa o alienigena e define sua posicao inicial."""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Carrega a imagem do alienigena e define seu atributo rect
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Inicia cada novo alienigena proximo a parte superior da tela
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height


        # Armazena a posicao exata do alienigena
        self.x = float(self.rect.x)

    def check_edges(self):
        """Devolve True se o alienigena estiver na borda da tela."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Move o alienigena para a direita."""
        self.x += (self.ai_settings.alien_speed_factor *
                   self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def blitme(self):
        """Desenha o alienigena em sua posicao actual."""
        self.screen.blit(self.image, self.rect)

