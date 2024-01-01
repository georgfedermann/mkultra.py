from .GameConfig import GameConfig
import pygame
from pygame.sprite import Sprite
import random

IMAGE_PATH = 'graphics/Fly/'

class Fly(Sprite):

    def __init__(self):
        super().__init__()

        self.fly1_surface = pygame.image.load(IMAGE_PATH + 'Fly1.png').convert_alpha()
        self.fly2_surface = pygame.image.load(IMAGE_PATH + 'Fly2.png').convert_alpha()
        self.fly_surfaces = [self.fly1_surface, self.fly2_surface]
        self.fly_animation_idx = 0

        self.image = self.fly_surfaces[self.fly_animation_idx]
        self.rect = self.image.get_rect(midbottom = (random.randint(900, 1100), GameConfig.FLIGHT_LEVEL))

        self.dx = random.choice([3,4,5,6])
        self.active = True

    def hit(self):
        print("Hit")
        self.active = False
        self.dy = 0
        self.image = pygame.transform.rotozoom(self.image, 180, 1)

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
