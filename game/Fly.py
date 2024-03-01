from .GameConfig import GameConfig
from .Monster import Monster
import pygame
from pygame.sprite import Sprite
import random

IMAGE_PATH = 'graphics/Fly'

class Fly(Monster):

    _punch_sound = None

    @property
    def punch_sound(self):
        if Fly._punch_sound is None:
            print(f'Loading punch sound from file')
            Fly._punch_sound = pygame.mixer.Sound('audio/punch.mp3')
            Fly._punch_sound.set_volume(0.5)
        else:
            print(f'Playing punch sound from memory')
        return Fly._punch_sound

    def __init__(self):
        super().__init__([f'{IMAGE_PATH}/fly1.png', f'{IMAGE_PATH}/fly2.png'],
                         (random.randint(900, 1100), GameConfig.FLIGHT_LEVEL))

        self.dx = random.choice([3,4,5,6])
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
