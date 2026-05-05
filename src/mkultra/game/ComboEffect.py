from math import cos, pi, sin

import pygame
from pygame.sprite import Sprite

from .GameConfig import GameConfig


class ComboEffect(Sprite):
    WIDTH = 170
    HEIGHT = 150
    COLORS = [
        (255, 246, 92),
        (255, 120, 28),
        (99, 238, 255),
        (255, 255, 255),
    ]

    def __init__(self, center, combo_size):
        super().__init__()
        self.center = center
        self.combo_size = combo_size
        self.started_at = pygame.time.get_ticks()
        self.duration = GameConfig.TRIPLE_COMBO_EFFECT_DURATION_MS if combo_size >= 3 else GameConfig.COMBO_EFFECT_DURATION_MS
        self.image = pygame.Surface((ComboEffect.WIDTH, ComboEffect.HEIGHT), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=center)

    def update(self):
        elapsed = pygame.time.get_ticks() - self.started_at
        if elapsed >= self.duration:
            self.kill()
            return

        progress = elapsed / self.duration
        self.image.fill((0, 0, 0, 0))
        star_count = 12 if self.combo_size >= 3 else 8
        radius = 30 + int(42 * progress)
        alpha = max(0, int(255 * (1 - progress)))
        spin = progress * pi * (4 if self.combo_size >= 3 else 2)

        for index in range(star_count):
            angle = spin + (2 * pi * index / star_count)
            x = ComboEffect.WIDTH // 2 + int(cos(angle) * radius)
            y = ComboEffect.HEIGHT // 2 + int(sin(angle) * (radius * 0.62))
            color = (*ComboEffect.COLORS[index % len(ComboEffect.COLORS)], alpha)
            self.draw_star((x, y), 8 if self.combo_size >= 3 else 6, color)

        if self.combo_size >= 3:
            ring_color = (255, 236, 72, int(160 * (1 - progress)))
            pygame.draw.ellipse(self.image, ring_color, (20, 30, 130, 80), 3)
            pygame.draw.ellipse(self.image, (255, 58, 24, int(120 * (1 - progress))), (10, 20, 150, 100), 2)

    def draw_star(self, center, radius, color):
        points = []
        for index in range(10):
            point_radius = radius if index % 2 == 0 else radius // 2
            angle = -pi / 2 + index * pi / 5
            points.append((center[0] + cos(angle) * point_radius, center[1] + sin(angle) * point_radius))
        pygame.draw.polygon(self.image, color, points)
