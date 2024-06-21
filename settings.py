class Settings:
    def __init__(self):
        # screen
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # ship
        self.ship_speed_factor = 1.5
        self.ship_limit = 3

        # bullet
        self.bullet_speed_factor = 1
        self.bullet_width = 300
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullet_allowed = 100

        # alien
        self.alien_speed_factor = 1
        self.alien_drop_speed = 10
        # fleet direction of 1 represents right; -1 represents left
        self.fleet_direction = 1