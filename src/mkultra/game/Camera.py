import pygame

from .GameConfig import GameConfig


class Camera:
    def __init__(self, level_width):
        self.level_width = level_width
        self.offset_x = 0

    def update(self, target_rect):
        target_x = target_rect.centerx - int(GameConfig.SCREEN_WIDTH * GameConfig.CAMERA_TARGET_X_RATIO)
        max_offset = max(0, self.level_width - GameConfig.SCREEN_WIDTH)
        self.offset_x = max(0, min(target_x, max_offset))

    def apply_rect(self, rect):
        return rect.move(-self.offset_x, 0)

    def visible_area(self):
        return pygame.Rect(self.offset_x, 0, GameConfig.SCREEN_WIDTH, GameConfig.SCREEN_HEIGHT)
