import pygame
from settings import Settings
from ship import Ship
import game_fuctions as gf
from pygame.sprite import Group
from game_stats import GameSats
from scoreboard import ScoreBoard
from button import Button


def run_game():
    # Inicializa o jogo e cria um objecto para a tela
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('Alien Invasion')

    time = pygame.time.Clock()

    # Cria uma instancia para armazenar dados estatisticos do jogo e cria
    # painel de pontuacao
    stats = GameSats(ai_settings)
    sb = ScoreBoard(ai_settings, screen, stats)
    # Cria uma espaconave, um grupo de projeteis e um grupo de
    # alienigenas
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()

    # Cria a frota de alienigenas
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Cria o botao play
    play_button = Button(ai_settings, screen, "Play")

    # Inicia o laco principal do jogo
    while True:

        time.tick(120)

        gf.check_events(ai_settings, screen, stats, sb, play_button, ship,
                        aliens, bullets)
        if stats.game_active:
            ship.update()
            bullets.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
                         play_button)


run_game()
