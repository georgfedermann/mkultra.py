from .GameConfig import GameConfig
import pygame
from pygame.sprite import Sprite
import random

IMAGE_PATH = 'graphics/Fly/'

class Fly(Sprite):

    _fly1_surface = None
    _fly2_surface = None

    _punch_sound = None

    @property
    def fly1_surface(self):
        if Fly._fly1_surface is None:
            Fly._fly1_surface = pygame.image.load(IMAGE_PATH + 'Fly1.png').convert_alpha()
        return Fly._fly1_surface

    @property
    def fly2_surface(self):
        if Fly._fly2_surface is None:
            Fly._fly2_surface = pygame.image.load(IMAGE_PATH + 'Fly2.png').convert_alpha()
        return Fly._fly2_surface

    @property
    def punch_sound(self):
        if Fly._punch_sound is None:
            Fly._punch_sound = pygame.mixer.Sound('audio/punch.mp3')
            Fly._punch_sound.set_volume(0.5)
        return Fly._punch_sound

    def __init__(self):
        super().__init__()

        self.fly_surfaces = [self.fly1_surface, self.fly2_surface]
        self.fly_animation_idx = 0

        self.image = self.fly_surfaces[self.fly_animation_idx]
        self.rect = self.image.get_rect(midbottom = (random.randint(900, 1100), GameConfig.FLIGHT_LEVEL))

        self.dx = random.choice([3,4,5,6])
        self.active = True

        self.damage_cooldown = 750
        self.damage_time = -1

    def can_do_damage(self, current_time):
        return current_time - self.damage_time > self.damage_cooldown

    def set_damage_time(self, current_time):
        self.damage_time = current_time

    def hit(self):
        print("Hit")
        self.active = False
        self.dy = 0
        self.image = pygame.transform.rotozoom(self.image, 180, 1)
        self.punch_sound.play()

    def update(self):
        if self.rect.right < 0 or self.rect.top > GameConfig.SCREEN_HEIGHT:
            self.kill()
        if self.active:
            self.rect.x -= self.dx
            self.image = self.fly_surfaces[int(self.fly_animation_idx)]
            self.fly_animation_idx = (self.fly_animation_idx + 0.1) % 2
        else:
            self.rect.y += self.dy
            self.dy += 1
