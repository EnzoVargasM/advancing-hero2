import os
from ..sprite import Sprite
import pygame


class PotionHeal(Sprite):
    """
    Represents a potion to heal the hero
    """
    def __init__(
        self,
        position,
        screen,
        path: str = 'advancing_hero/images/sprites/potions/potion_heal/',
    ) -> None:
        super().__init__(path=os.path.abspath(path), position=position)

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.position = position
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.heal = 35
        self.music_path = os.path.abspath('advancing_hero/songs/item.wav')
        self.screen = screen

    def update(self, player, stage):
        super().update()
        self.rect.y += stage.scroll_amount
        self.player_collision(player)
        if self.rect.colliderect(self.screen.get_rect()) == 0:
            self.kill()

    def player_collision(self, player):
        if self.rect.colliderect(player.rect):
            player.heal(self.heal)
            self.play_music()
            self.kill()

    def play_music(self):
        sound = pygame.mixer.Sound(self.music_path)
        sound.set_volume(0.4)
        pygame.mixer.Channel(7).play(sound)
