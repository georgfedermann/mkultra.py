from .GameConfig import GameConfig
import pygame
from pygame.sprite import Sprite
import random

IMAGE_PATH = 'graphics/snail/'

class Snail(Sprite):

    def __init__(self):
        super().__init__()

        self.snail1_surface = pygame.image.load(IMAGE_PATH + 'snail1.png').convert_alpha()
        self.snail2_surface = pygame.image.load(IMAGE_PATH + 'snail2.png').convert_alpha()
        self.snail_surfaces = [self.snail1_surface, self.snail2_surface]
        self.snail_animation_idx = 0

        self.image = self.snail_surfaces[self.snail_animation_idx]
        self.rect = self.image.get_rect(midbottom = (random.randint(900, 1100), GameConfig.GROUND_LEVEL))

        self.damage_cooldown = 750
        self.damage_time = -1

    def can_do_damage(self, current_time):
        return current_time - self.damage_time > self.damage_cooldown

    def set_damage_time(self, current_time):
        self.damage_time = current_time

    def update(self):
        if self.rect.right < 0:
            self.kill()
        self.rect.x -= 4
        self.image = self.snail_surfaces[int(self.snail_animation_idx)]

        self.snail_animation_idx = (self.snail_animation_idx + 0.1) % 2

