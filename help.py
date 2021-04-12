import sys
import pygame

class Configuracoes:
    def __init__(self):
        self.largura = 1200
        self.altura = 600
        self.cor = (135, 206, 235)


class Espaconave:
    def __init__(self, tela):
        """Inicializa a espaconave e define sua posicao inicial"""
        self.tela = tela

        # Carrega a imagem da espaconave e obtem seu rect
        self.imagem = pygame.image.load('./images/ship.bmp')
        self.rect = self.imagem.get_rect()
        self.tela_rect = tela.get_rect()

        # Inicia cada nova espaconave a parte inferior da tela
        self.rect.centerx = self.tela_rect.centerx  # centraliza no eixo x
        self.rect.bottom = self.tela_rect.bottom  # coloca no linha de baixo

    def desenha(self):
        """Desenha a espaconave em sua posicao actual"""
        self.tela.blit(self.imagem, self.rect)



def inicia_jogo():

    pygame.init()  # Inicia o jogo
    config = Configuracoes()
    pygame.display.set_caption('Meu primeiro jogo')  # define o titulo da janela

    while True:

        # Laco para escutar os eventos do usuario
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


        screen.fill(bg_color) # define a cor na tela
        pygame.display.flip() # atualiza a tela

inicia_jogo()