import os
import math
from . import Player
from .hero_weapons.mega_blast import MegaBlast
from .hero_weapons.regular_blast import RegularBlast
import pygame

weapons = {'regular_blast': RegularBlast, 'mega_blast': MegaBlast}


class PlayerMage(Player):

    def __init__(
            self,
            position,
            settings,
            stage,
            screen,
    ) -> None:
        super().__init__(
            position=position,
            settings=settings,
            stage=stage,
            screen=screen,
            path=os.path.abspath('advancing_hero/images/sprites/player/'),
            max_health=100,
        )
        self.special_attack_cooldown = 0
        self.current_weapon = 'regular_blast'
        self.time_charging = -15
        # Cooldowns unique to this hero
        self.attack_cooldown_heal = 0
        self.attack_cooldown_mega = 0
        self.speed_buff_cooldown = 0

    def handle_weapon(self):

        key = pygame.key.get_pressed()
        if key[pygame.K_c]:
            if self.current_weapon == 'regular_blast' and self.attack_cooldown == 0 and len(
                    self.projectiles.sprites()) < 2:
                if self.time_charging > 60:
                    if self.time_charging > 120:
                        if self.time_charging >= 150:
                            pass
                        else:
                            if self.frame_counter % 15 == 0:
                                self.time_charging += 1
                    else:
                        if self.frame_counter % 5 == 0:
                            self.time_charging += 1
                else:
                    self.time_charging += 1
                print(self.time_charging)
            if self.current_weapon == 'mega_blast' and self.attack_cooldown_mega == 0 and len(
                    self.projectiles.sprites()) < 2:
                if self.time_charging > 60:
                    if self.time_charging > 120:
                        if self.frame_counter % 15 == 0:
                            self.time_charging += 1
                    else:
                        if self.frame_counter % 5 == 0:
                            self.time_charging += 1
                else:
                    self.time_charging += 1
                print(self.time_charging)
            if self.current_weapon == 'heal' and self.attack_cooldown_heal == 0:
                if self.time_charging > 60:
                    if self.time_charging > 120:
                        if self.frame_counter % 15 == 0:
                            self.time_charging += 1
                    else:
                        if self.frame_counter % 5 == 0:
                            self.time_charging += 1
                else:
                    self.time_charging += 1
                print(self.time_charging)
        if not key[pygame.K_c] and self.time_charging > 0:
            if self.current_weapon == 'regular_blast':
                self.attack_cooldown += self.time_charging
                self.weapon = weapons[self.current_weapon]((self.rect.centerx, self.rect.centery),
                                                           self.moving_direction, self.settings, self.time_charging)
                self.projectiles.add(self.weapon)
            elif self.current_weapon == 'mega_blast':
                self.attack_cooldown_mega += self.time_charging * 4
                self.weapon = weapons[self.current_weapon]((self.rect.centerx, self.rect.centery),
                                                           self.moving_direction, self.settings, self.time_charging)
                self.projectiles.add(self.weapon)
            elif self.current_weapon == 'heal':
                self.attack_cooldown_heal += self.time_charging * 5
                # Buffs
                self.heal(self.time_charging/20)
                self.speed_base += self.time_charging/5
                self.speed_buff_cooldown = 60
                print(self.time_charging/10)
            self.time_charging = -15
        if key[pygame.K_v] and self.changing_weapon_cooldown == 0:
            if self.current_weapon == 'regular_blast':
                self.current_weapon = 'mega_blast'
            elif self.current_weapon == 'mega_blast':
                self.current_weapon = 'heal'
            elif self.current_weapon == 'heal':
                self.current_weapon = 'regular_blast'
            self.changing_weapon_cooldown += 15

    def update_cooldown(self):
        if self.changing_weapon_cooldown > 0:
            self.changing_weapon_cooldown -= 1
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.attack_cooldown_heal > 0:
            self.attack_cooldown_heal -= 1
        if self.attack_cooldown_mega > 0:
            self.attack_cooldown_mega -= 1
        if self.speed_buff_cooldown > 0:
            self.speed_buff_cooldown -= 1
        if self.speed_buff_cooldown == 0:
            self.speed_base = self.hero_base_speed

    def handle_movement(self):
        dx = 0
        dy = 0
        moving_flag = False  # Handles multiple key presses
        key = pygame.key.get_pressed()
        if not key[pygame.K_c]:
            if key[pygame.K_w]:
                self.walk_animation(7, 1)
                moving_flag = True
                dy -= 1
            if key[pygame.K_a]:
                if not moving_flag:
                    self.walk_animation(4, 2)
                moving_flag = True
                dx -= 1
            if key[pygame.K_d]:
                if not moving_flag:
                    self.walk_animation(4, 4, flip=True)
                dx += 1
                moving_flag = True
            if key[pygame.K_s]:
                if not moving_flag:
                    self.walk_animation(1, 3)
                dy += 1

        if dx == 0 and dy == 0:
            self.walking_framerate = 0
            # If we were walking and stopped, keep looking to
            # the direction we were looking before
            if self.moving_direction == 1:
                self.image_frame = 7
                self.update_rect()
            if self.moving_direction == 2:
                self.image_frame = 4
                self.update_rect()
            if self.moving_direction == 3:
                self.image_frame = 1
                self.update_rect()
            if self.moving_direction == 4:
                self.image_frame = 4
                self.update_rect(flip=True)

        for tile in self.stage.tile_list:
            # Check only blocks which are on screen and are interactable
            if tile[1].bottom > 0 and tile[
                1].top < self.settings.screen_height and tile[
                2].is_interactable:

                # First run block interaction code. The collision is checked with
                # the player's standing point
                if tile[1].colliderect(self.rect.x,
                                       self.rect.y + 3 * self.rect.height / 4,
                                       self.rect.width, self.rect.height / 4):
                    tile[2].player_interaction(self)

                # Then check if it's solid. We do it on that order in case
                # the block changes the player's speed.
                if tile[2].is_solid and (dx or dy):
                    # Check collision in x direction
                    delta_x = self.speed * dx / math.sqrt(dx * dx + dy * dy)
                    delta_y = self.speed * dy / math.sqrt(dx * dx + dy * dy)
                    if tile[1].colliderect(self.rect.x + delta_x, self.rect.y,
                                           self.rect.width, self.rect.height):
                        dx = 0
                    # Check for collision in y direction
                    if tile[1].colliderect(self.rect.x, self.rect.y + delta_y,
                                           self.rect.width, self.rect.height):
                        dy = 0

        if dx or dy:
            self.rect.x += self.speed * dx / math.sqrt(dx * dx + dy * dy)
            self.rect.y += self.speed * dy / math.sqrt(dx * dx + dy * dy)

        if self.rect.bottom > self.settings.screen_height:
            self.rect.bottom = self.settings.screen_height
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.right > self.settings.screen_width:
            self.rect.right = self.settings.screen_width
        if self.rect.left < 0:
            self.rect.left = 0


