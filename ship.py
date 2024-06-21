import pygame


class Ship():
    def __init__(self, screen, ai_settings):
        self.screen = screen
        self.ai_settings = ai_settings

        self.image = pygame.image.load('./images/plane.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery
        self.rect.bottom = self.screen_rect.bottom

        self.center = float(self.rect.centerx)
        self.centery = float(self.rect.centery)

        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def blitme(self):
        self.screen.blit(self.image, self.rect)


    def update(self):
        if self.moving_right and self.rect.centerx < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.centerx > 0:
            self.center -= self.ai_settings.ship_speed_factor
        if self.moving_up and self.rect.centery > 0:
            self.centery -= self.ai_settings.ship_speed_factor
        if self.moving_down and self.rect.centery < self.screen_rect.bottom:
            self.centery += self.ai_settings.ship_speed_factor

        self.rect.centerx = self.center
        self.rect.centery = self.centery

    def center_ship(self):
        self.center = self.screen_rect.centerx
