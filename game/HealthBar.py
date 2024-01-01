from .GameConfig import GameConfig
import pygame
from pygame.sprite import Sprite

class HealthBar(Sprite):

    def __init__(self, alien):
        super().__init__()
        self.alien = alien
        self.image = pygame.Surface((GameConfig.HEALTHBAR_WIDTH, 10))
        self.rect = self.image.get_rect(topleft = (10, 10))

    def update(self):
        pygame.draw.rect(self.image, (255, 0, 0), (0, 0, GameConfig.HEALTHBAR_WIDTH, 10))
        pygame.draw.rect(self.image, (0, 255, 0), (0, 0, GameConfig.HEALTHBAR_WIDTH / 100 * self.alien.life_energy, 10))

    def set_alien(self, alien):
        self.alien = alien
