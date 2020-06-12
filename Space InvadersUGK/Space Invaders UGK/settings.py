class Settings():
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (77, 77, 77)

        # settings ship
        self.ship_speed = 0.5
        self.ship_limit = 3

        # settings bullet
        self.bullet_speed = 1
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = (120, 180, 20)

        # settings enemy
        self.enemy_speed = 0.1
        self.fleet_drop_speed = 8
        self.fleet_direction = 4

        # hard game
        self.speedup_scale = 1.1
        # cost enemy
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3.0
        self.enemy_speed_factor = 1.0

        self.fleet_direction = 4
        # score
        self.enemy_points = 10

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.enemy_speed_factor *= self.speedup_scale
        self.enemy_points = int(self.enemy_points * self.score_scale)

