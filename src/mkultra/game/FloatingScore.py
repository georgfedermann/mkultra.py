import pygame
from pygame.sprite import Sprite

from mkultra.assets import load_font

from .GameConfig import GameConfig


class FloatingScore(Sprite):
    GOLD = (255, 216, 64)
    CYAN = (84, 244, 255)
    RED = (255, 62, 28)
    SHADOW = (18, 8, 4)

    def __init__(self, center, points, combo_size):
        super().__init__()
        self.center = center
        self.points = points
        self.combo_size = combo_size
        self.started_at = pygame.time.get_ticks()
        self.font = load_font('font/Pixeltype.ttf', 42 if combo_size >= 3 else 34)
        self.image = pygame.Surface((1, 1), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=center)

    def update(self):
        elapsed = pygame.time.get_ticks() - self.started_at
        if elapsed >= GameConfig.FLOATING_SCORE_DURATION_MS:
            self.kill()
            return

        progress = elapsed / GameConfig.FLOATING_SCORE_DURATION_MS
        alpha = max(0, int(255 * (1 - progress)))
        y_offset = int(42 * progress)
        color = FloatingScore.RED if self.combo_size >= 3 else FloatingScore.GOLD
        text = f'+{self.points} COMBO'

        text_surface = self.font.render(text, False, color)
        shadow_surface = self.font.render(text, False, FloatingScore.SHADOW)
        width = text_surface.get_width() + 12
        height = text_surface.get_height() + 10
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)

        if self.combo_size >= 3:
            pygame.draw.rect(self.image, (*FloatingScore.CYAN, int(75 * (1 - progress))), self.image.get_rect(), 2)

        shadow_surface.set_alpha(alpha)
        text_surface.set_alpha(alpha)
        self.image.blit(shadow_surface, (8, 7))
        self.image.blit(text_surface, (6, 5))
        self.rect = self.image.get_rect(center=(self.center[0], self.center[1] - 54 - y_offset))
