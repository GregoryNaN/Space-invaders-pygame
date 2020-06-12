import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    # move bullet
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # create bullet in start position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
                                self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # float format
        self.y = float(self.rect.y)

    def update(self):
        self.y -= self.settings.bullet_speed
        # update position
        self.rect.y = self.y

    def draw_bullet(self):
        # out bullet on screen
        pygame.draw.rect(self.screen, self.color, self.rect)

