import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from enemy import Enemy


class SpaceIndavers:

    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode([800, 600])
        pygame.display.set_caption("SpaceIndavers")

        self.settings = Settings()
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.enemy = pygame.sprite.Group()

        self._create_fleet()
        # create button play
        self.play_button = Button(self, "Play")

    def _create_fleet(self):
        # create enemy
        enemy = Enemy(self)
        enemy_width, enemy_height = enemy.rect.size
        enemy_width = enemy.rect.width
        aviilable_space_x = self.settings.screen_width - (2 * enemy_width)
        number_enemy_x = aviilable_space_x // (2 * enemy_width)

        ship_heignt = self.ship.rect.height
        aviilable_space_y = (self.settings.screen_height -
                             (3 * enemy_height) - 2 * ship_heignt)
        number_rows = aviilable_space_y // (2 * enemy_height)

        # create first enemy fleet
        for row_number in range(number_rows):
            for enemy_number in range(number_enemy_x):
                self._create_enemy(enemy_number, row_number)

    def _create_enemy(self, enemy_number, row_number):
        # create enemy
        enemy = Enemy(self)
        enemy_width, enemy_height = enemy.rect.size
        enemy.x = enemy_width + 2 * enemy_width * enemy_number
        enemy.rect.x = enemy.x
        enemy.rect.y = enemy.rect.height + 2 * enemy.rect.height * row_number
        self.enemy.add(enemy)

    def _change_fleet_edges(self):
        for enemy in self.enemy.sprites():
            if enemy.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for enemy in self.enemy.sprites():
            enemy.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))

    def run_game(self):
        # start main round game
        while True:
            self._update_enemy()
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()

            self._update_screen()

    def _update_bullets(self):
        self.bullets.update()
        # delete bullet
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        print(len(self.bullets))
        # delete enemy
        self._check_bullet_enemy_collisions()

    def _check_bullet_enemy_collisions(self):
        # delete ,bullet and enemy
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.enemy, True, True)
        if collisions:
            for enemy in collisions.values():
                self.stats.score += self.settings.enemy_points * len(enemy)
            self.sb.prep_score()
        if not self.enemy:
            # create new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # + level
            self.stats.level += 1
            self.sb.prep_level()

    def _update_enemy(self):
        self._change_fleet_edges()
        self.enemy.update()
        if pygame.sprite.spritecollideany(self.ship, self.enemy):
            self._ship_hit()
        self._check_enemy_bottom()

    def _ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            self.enemy.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            # pause
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_enemy_bottom(self):
        screen_rect = self.screen.get_rect()
        for enemy in self.enemy.sprites():
            if enemy.rect.bottom >= screen_rect.bottom:
                #
                self._ship_hit()
                break

    def _check_events(self):
        # history screen and keyboard

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_play_button(self, mouse_pos):

        if self.play_button.rect.collidepoint(mouse_pos):
            # delete static
            button_clicked = self.play_button.rect.collidepoint(mouse_pos)
            if button_clicked and not self.stats.game_active:
                self.settings.initialize_dynamic_settings()
                self.stats.reset_stats()
                self.stats.game_active = True
                self.sb.prep_level()
                self.sb.prep_score()

                pygame.mouse.set_visible(False)

                self.enemy.empty()
                self.bullets.empty()

                self._create_fleet()
                self.ship.center_ship()

    def _check_keydown_events(self, event):
        # reaction on keystroke button
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        # exit with button esc
        elif event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        # reaction on don't keystroke button
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        # create new bullet
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def _update_screen(self):

        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.enemy.draw(self.screen)
        self.sb.show_score()
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


if __name__ == '__main__':
    # create and start game
    ai = SpaceIndavers()
    ai.run_game()
