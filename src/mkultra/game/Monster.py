from pygame.sprite import Sprite

from mkultra.assets import load_image

from .GameConfig import GameConfig


class Monster(Sprite):

    image_cache = {}

    def __init__(self, image_paths, start_position, images=None):
        super().__init__()
        self.animation_idx = 0
        self.image_paths = image_paths
        self.animation_images = images
        if self.animation_images:
            self.image = self.animation_images[int(self.animation_idx)]
        else:
            Monster.load_images(image_paths)
            self.image = Monster.image_cache[self.image_paths[int(self.animation_idx)]]
        self.rect = self.image.get_rect(midbottom = start_position)
        self.active = True

    @classmethod
    def load_images(cls, image_paths):
        for path in image_paths:
            if path not in cls.image_cache:
                cls.image_cache[path] = load_image(path)

    def update_animation(self):
        frame_count = len(self.animation_images) if self.animation_images else len(self.image_paths)
        self.animation_idx = (self.animation_idx + GameConfig.ANIMATION_SPEED) % frame_count
        if self.animation_images:
            self.image = self.animation_images[int(self.animation_idx)]
        else:
            self.image = Monster.image_cache[self.image_paths[int(self.animation_idx)]]
