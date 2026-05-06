import pygame
from pygame.sprite import Sprite


class Platform(Sprite):
    def __init__(self, rect, velocity=(0, 0), movement_bounds=None, color=(86, 82, 74), visible=True):
        super().__init__()
        self.rect = pygame.Rect(rect)
        self.velocity = pygame.Vector2(velocity)
        self.movement_bounds = pygame.Rect(movement_bounds) if movement_bounds else None
        self.visible = visible
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.image.fill(color)
        pygame.draw.rect(self.image, (130, 124, 106), self.image.get_rect(), 2)

    def update(self):
        if self.velocity.length_squared() == 0:
            return

        self.rect.x += int(self.velocity.x)
        self.rect.y += int(self.velocity.y)

        if self.movement_bounds and not self.movement_bounds.contains(self.rect):
            if self.rect.left < self.movement_bounds.left or self.rect.right > self.movement_bounds.right:
                self.velocity.x *= -1
            if self.rect.top < self.movement_bounds.top or self.rect.bottom > self.movement_bounds.bottom:
                self.velocity.y *= -1
            self.rect.clamp_ip(self.movement_bounds)
