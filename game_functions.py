import sys
from time import sleep

import pygame

from alien import Alien
from bullet import Bullet


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        print('you press up')
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        print('you press down')
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        firing_bullet(bullets, ai_settings, screen, ship)
    elif event.key == pygame.K_q:
        print('I execution')
        sys.exit()


def firing_bullet(bullets, ai_settings, screen, ship):
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False


def check_events(ai_settings, screen, ship, bullets, play_button, game_stats, aliens, sb):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(game_stats, play_button, mouse_x, mouse_y, aliens, bullets, ai_settings, screen, ship, sb)


def check_play_button(game_stats, play_button, mouse_x, mouse_y, aliens, bullets, ai_settings, screen, ship, sb):
    """ start a new game when the player clicks play button """
    button_click = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_click and not game_stats.game_active:
        # reset the game setting
        ai_settings.initialize_dynamic_settings()
        # hide the mouse cursor
        pygame.mouse.set_visible(False)
        # reset the game statistics
        game_stats.reset_stats()
        game_stats.game_active = True

        # Reset the scoreboard images.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # create a new fleet and center the ship
        create_fleet(ai_settings, screen, aliens, ship)


def update_screen(ai_settings, screen, ship, bullets, aliens, button, game_stats, sb):
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()

    if not game_stats.game_active:
        button.draw_button()

    pygame.display.flip()


def update_bullets(bullets, aliens, ai_settings, screen, ship, stats, sb):
    # update position
    bullets.update()
    # get rid of bullets that have disappeared.
    for bullet in bullets.copy():
        if bullet.rect.bottom < 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, aliens, ship, bullets, stats, sb)


def check_bullet_alien_collisions(ai_settings, screen, aliens, ship, bullets, stats, sb):
    # check for any bullets that have hit alien
    # if so, get rid of the bullet and the alien.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # destroy  existing bullets, speed up game and create new fleet.
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, aliens, ship)



def update_aliens(ai_settings, aliens, ship, stats, screen, bullets, sb):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)
    # look for aliens hitting the bottom of the screen
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb)


def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.alien_drop_speed
    ai_settings.fleet_direction *= -1


def create_fleet(ai_settings, screen, aliens, ship):
    alien = Alien(screen, ai_settings)
    alien_width = alien.rect.width
    numbers_aliens_x = get_aliens_number_x(ai_settings, alien_width)
    number_rows = get_number_rows(ai_settings, alien.rect.height, ship.rect.height)
    # create the first row of aliens:
    for number_row in range(number_rows):
        for alien_number in range(numbers_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, number_row)


def get_aliens_number_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - (2 * alien_width)
    numbers_aliens_x = int(available_space_x / (2 * alien_width))
    return numbers_aliens_x


def get_number_rows(ai_settings, alien_height, ship_height):
    available_space_y = ai_settings.screen_height - 3 * alien_height - ship_height
    numbers_rows = int(available_space_y / (2 * alien_height))
    return numbers_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    alien = Alien(screen, ai_settings)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_number * alien_width
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb):
    # respond to ship being hit by alien
    if stats.ships_left > 0:
        # decrement ship left
        stats.ships_left -= 1

        sb.prep_ships()

        # empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()

        create_fleet(ai_settings, screen, aliens, ship)
        ship.center_ship()

        # pause
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb):
    """ checks if any aliens have been reaches the bottom of the screen """
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # treat it the same as if the ship got hit.
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)
            break


def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
