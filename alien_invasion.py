import pygame
from pygame.sprite import Group

import game_functions as gf
from button import Button
from game_stats import GameStats
from scoreboard import Scoreboard
from settings import Settings
from ship import Ship


def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("外星人入侵地球")

    # make a play button
    play_button = Button(ai_settings, screen, 'play')

    # Make a ship, a group of bullets, and a fleet of aliens.
    ship = Ship(screen, ai_settings)
    # alien = Alien(screen, ai_settings)
    bullets = Group( )
    aliens = Group()
    # create an instance to store game statistics and create a scoreboard
    game_stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, game_stats)

    # creating the fleet of aliens
    gf.create_fleet(ai_settings, screen, aliens, ship)

    while True:
        gf.check_events(ai_settings, screen, ship, bullets, play_button, game_stats, aliens, sb)

        if game_stats.game_active:
            ship.update()
            gf.update_bullets(bullets, aliens, ai_settings, screen, ship, game_stats, sb)
            gf.update_aliens(ai_settings, aliens, ship, game_stats, screen, bullets, sb)

        gf.update_screen(ai_settings, screen, ship, bullets, aliens, play_button, game_stats, sb)


run_game()
