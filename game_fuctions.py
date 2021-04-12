import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def check_keydown_events(event, ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Responde a pressionametos de tecla."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit('Volte sempre...')
    elif event.key == pygame.K_p:
        start_game(ai_settings, screen, stats, sb, ship, aliens, bullets)

def fire_bullet(ai_settings, screen, ship, bullets):
    """Dispara um projetil se o limite ainda nao foi alcancado."""
    # Cria um novo projetil e o adiciona ao grupo de projeteis
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def check_keyup_events(event, ship):
    """Responde a solturas de tecla."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """Responde a eventos de pressionamento de teclas e de mouse."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, sb, ship, aliens, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship,
                              aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship,
                      aliens, bullets, mouse_x, mouse_y):
    """Inicia um novo jogo quando o jogador clicar em Play."""
    buttom_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if buttom_clicked:
        start_game(ai_settings, screen, stats, sb,  ship, aliens, bullets)

def start_game(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Exercicio 14.1 INICIA O JOGO COM A TECLA P"""
    if not stats.game_active:
        # Reinicia as configuracoes do jogo
        ai_settings.initialize_dynamic_settings()

        # Oculta o cursos do mouse
        pygame.mouse.set_visible(False)

        # Reinicia os dados estatisticos do jogo
        stats.reset_stats()
        stats.high_score = int(load_max_point()) if load_max_point() != '' else 0
        stats.game_active = True

        # Reinicia as imagens do painel de pontuacao
        sb.prep_images()

        # Esvazia a lista de alienigenas e de projeteis
        aliens.empty()
        bullets.empty()

        # Cria uma nova frota e centraliza a espaconave
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """Atualiza as imagens na tela e alterna para a nova tela"""
    # Redesenha a tela a cada passagem pelo laco
    screen.fill(ai_settings.bg_color)

    # Desenha a informacao sobre pontuacao
    sb.show_score()

    # Redesenha todos os projeteis atras da espaconave e dos alienigenas
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)

    # Desenha o botao Play se o jogo estiver inativo
    if not stats.game_active:
        play_button.draw_button()

    # Deixa a tela mais recente visivel
    pygame.display.flip()

def update_bullets(ai_settings,screen, stats, sb, ship, aliens, bullets):
    """Atualiza a posicao dos projeteis e se livra dos porjeteis
    antigos."""

    bullets.update()

    # Livra-se dos projeteis que desapareceram
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens,
                                  bullets)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens,
                                  bullets):
    """Responde a colicoes entre projeteis e alienigenas."""

    # Remove qualquer projetil e alienigena que tenham colidido
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # Se a frota for destruida, inicia um novo nivel
        bullets.empty()
        ai_settings.increase_speed()

        # Aumenta o nivel
        start_new_level(ai_settings, screen, stats, sb, ship, aliens)


def start_new_level(ai_settings, screen, stats, sb, ship, aliens):
    """Inicia um novo nivel do jogo."""
    stats.level += 1
    sb.prep_level()
    create_fleet(ai_settings, screen, ship, aliens)


def check_high_score(stats, sb):
    """Verifica se ha uma nova pontuacao maxima."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        update_points(stats.high_score)
        sb.prep_high_score()

def get_number_aliens_x(ai_settings, alien_width):
    """Determina o numero de alienigenas que cabem em uma linha."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    """Determina o numero de linhas com alienigenas que cabem na tela."""
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    # Cria um alienigena e o posiciona na linha
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship,  aliens):
    """Cria uma frota completa de alienigenas."""
    # Cria um alienigena e calcula o numero de alienigenas em uma linha
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # Cria a frota de alienigenas
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
           create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settins, aliens):
    """Responde apropriadamente se algum alienigena alcancou uma
    borda."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settins, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """Faz toda a frota descer e muda a sua direcao."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def update_aliens(ai_settings,stats, screen, sb, ship, aliens, bullets):
    """Verifica se a frota esta em duas bordas
    e entao atualiza as posicoes de todos os alienigenas da frota."""

    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Verifica se houve colisoes entre alienigenas e a espaconave
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)

    # Verifica se ha algum alienigena que atingiu a parte inferior da tela
    check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets)

def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """Verifica se algum alienigena alcancou a parte inferior da tela"""

    screen_rect = screen.get_rect()

    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Trata esse caso do mesmo modo que e feito quando a espaconave
            # e atingida
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
            break


def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """Responde ao fato de a espaconave ter sido atingida por um
    alienigena"""

    if stats.ships_left > 0:
        # Decrementa ships_left
        stats.ships_left -= 1

        # Atualiza o painel de pontuacoes
        sb.prep_ships()

        # Esvazia a lista de alienigena e de projeteis
        aliens.empty()
        bullets.empty()

        # Cria uma nova frota e centraliza a espaconave
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Faz uma pausa
        sleep(1)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def load_max_point():
    """Carrega os pontos maximos."""
    while True:
        try:
            file = open('data/max_points.txt', 'r')
        except:
            file = open('data/max_points.txt', 'w')
        else:
            return file.readline()


def update_points(points):
    """Atualiza os pontos maximos."""
    file = open('data/max_points.txt', 'w')
    file.write(str(points))
