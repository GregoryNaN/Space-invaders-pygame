import pygame
from pygame.sprite import Sprite


class Enemy(Sprite):

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # download images
        self.image = pygame.image.load("images/enemy1.png")
        self.rect = self.image.get_rect()

        # every new enemy show in left up
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        # keep position
        self.x = float(self.rect.x)

    def update(self):
        self.x += (self.settings.enemy_speed *
                   self.settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
