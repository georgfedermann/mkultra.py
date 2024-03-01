from .GameConfig import GameConfig
from .Monster import Monster
import pygame
from pygame.sprite import Sprite
import random

IMAGE_PATH = 'graphics/snail'

class Snail(Monster):

    def __init__(self):
        super().__init__([f'{IMAGE_PATH}/snail1.png', f'{IMAGE_PATH}/snail2.png'],
                         (random.randint(900, 1100), GameConfig.GROUND_LEVEL))

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
        self.update_animation()
