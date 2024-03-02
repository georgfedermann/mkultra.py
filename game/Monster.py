from .GameConfig import GameConfig
import pygame
from pygame.sprite import Sprite

class Monster(Sprite):

    image_cache = {}

    def __init__(self, image_paths, start_position):
        super().__init__()
        Monster.load_images(image_paths)
        self.animation_idx = 0
        self.image_paths = image_paths
        self.image = Monster.image_cache[self.image_paths[int(self.animation_idx)]]
        self.rect = self.image.get_rect(midbottom = start_position)
        self.active = True

    @classmethod
    def load_images(cls, image_paths):
        for path in image_paths:
            if path not in cls.image_cache:
                cls.image_cache[path] = pygame.image.load(path).convert_alpha()

    def update_animation(self):
        self.animation_idx = (self.animation_idx + GameConfig.ANIMATION_SPEED) % 2
        self.image = Monster.image_cache[self.image_paths[int(self.animation_idx)]]

