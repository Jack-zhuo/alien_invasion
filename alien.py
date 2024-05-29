import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    def __init__(self, screen, ai_settings):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # loading alien image and set its rect attribute
        self.image = pygame.image.load('./images/alien.png')
        self.rect = self.image.get_rect()

        # placing alien in screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # store alien exact position
        self.x = float(self.rect.x)

    def blitme(self):
        self.screen.blit(self.image, self.rect)
