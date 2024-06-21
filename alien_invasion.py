import pygame
from settings import Settings
from ship import Ship
from alien import Alien
from game_stats import GameStats
import game_functions as gf
from pygame.sprite import Group

def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("外星人入侵地球")

    # Make a ship, a group of bullets, and a fleet of aliens.
    ship = Ship(screen, ai_settings)
    # alien = Alien(screen, ai_settings)
    bullets = Group()
    aliens = Group()
    # create a instance to store game statistics
    game_stats = GameStats(ai_settings)

    # creating the fleet of aliens
    gf.create_fleet(ai_settings, screen, aliens, ship)

    while True:
        gf.check_events(ai_settings, screen, ship, bullets)

        if game_stats.game_active:
            ship.update()
            gf.update_bullets(bullets, aliens, ai_settings, screen, ship)
            gf.update_aliens(ai_settings, aliens, ship, game_stats, screen, bullets)

        gf.update_screen(ai_settings, screen, ship, bullets,aliens)

run_game()

