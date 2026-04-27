import pygame
from pygame.sprite import Sprite

from mkultra.assets import load_image

from .GameConfig import GameConfig

_IMAGE_PATH = 'graphics/snail_explosion.png'

class SnailExplosion(Sprite):

    image_cache = {}

    def __init__(self, position):
        super().__init__()

        # Load the sprite sheet if not already cached
        if _IMAGE_PATH not in SnailExplosion.image_cache:
            sprite_sheet = load_image(_IMAGE_PATH)
            SnailExplosion.image_cache[_IMAGE_PATH] = sprite_sheet

        # Generate individual frames from the sprite sheet
        self.frames = self._generate_frames()
        self.animation_idx = 0
        self.image = self.frames[self.animation_idx]
        self.rect = self.image.get_rect(center=position)
        self.animation_speed = GameConfig.ANIMATION_SPEED
        self.frame_count = 0
        self.completed = False

    def _generate_frames(self):
        """Generate 12 individual frames from the sprite sheet."""
        frames = []
        sprite_sheet = SnailExplosion.image_cache[_IMAGE_PATH]

        # Sprite sheet dimensions: 1152x96, each frame is 96x96
        frame_width = 96
        frame_height = 96

        for i in range(12):
            # Calculate the position of each frame in the sprite sheet
            x = i * frame_width
            y = 0

            # Extract the frame
            frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            frame.blit(sprite_sheet, (0, 0), (x, y, frame_width, frame_height))
            frames.append(frame)

        return frames

    def update(self):
        """Update animation frame."""
        self.frame_count += 1

        # Advance animation at the configured speed
        if self.frame_count % int(1 / self.animation_speed) == 0:
            self.animation_idx += 1
            if self.animation_idx >= len(self.frames):
                self.animation_idx = len(self.frames) - 1
                self.completed = True
            self.image = self.frames[self.animation_idx]

    def is_complete(self):
        """Check if animation has completed."""
        return self.completed
