import random

import pygame

from mkultra.assets import load_sound

from .GameConfig import GameConfig
from .Monster import Monster
from .PlatformerAtlas import platformer_atlas


class Fly(Monster):

    _punch_sound = None

    @property
    def punch_sound(self):
        if Fly._punch_sound is None:
            Fly._punch_sound = load_sound('audio/punch.mp3')
            Fly._punch_sound.set_volume(0.5)
        return Fly._punch_sound

    def __init__(self, start_x=None):
        if start_x is None:
            start_x = random.randint(GameConfig.SPAWN_X_MIN, GameConfig.SPAWN_X_MAX)

        atlas = platformer_atlas()
        super().__init__(
            [],
            (start_x, GameConfig.FLIGHT_LEVEL),
            images=[atlas.sprite('fly_1'), atlas.sprite('fly_2')],
        )

        self.dx = random.choice([3, 4, 5, 6])
        self.active = True

        self.damage_cooldown = 750
        self.damage_time = -1

    def can_do_damage(self, current_time):
        return current_time - self.damage_time > self.damage_cooldown

    def set_damage_time(self, current_time):
        self.damage_time = current_time

    def hit(self):
        self.active = False
        self.dy = 0
        self.image = pygame.transform.rotozoom(self.image, 180, 1)
        self.punch_sound.play()

    def update(self):
        if self.rect.right < 0 or self.rect.top > GameConfig.SCREEN_HEIGHT:
            self.kill()
        if self.active:
            self.rect.x -= self.dx
            self.update_animation()
        else:
            self.rect.y += self.dy
            self.dy += 1
