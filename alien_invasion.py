import pygame
from settings import Settings
from ship import Ship
from alien import Alien
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

    # creating the fleet of aliens
    gf.create_fleet(ai_settings, screen, aliens, ship)

    while True:
        gf.check_events(ai_settings, screen, ship, bullets)
        ship.update()
        gf.update_bullets(bullets)

        gf.update_screen(ai_settings, screen, ship, bullets,aliens)

run_game()

