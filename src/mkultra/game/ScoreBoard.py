from pathlib import Path

import pygame
from pygame.sprite import Sprite

_ASSET_DIR = Path(__file__).resolve().parent.parent.parent.parent / "assets"

class ScoreBoard(Sprite):

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.font = pygame.font.Font(str(_ASSET_DIR / 'font' / 'Pixeltype.ttf'), 30)
        self.image = self.font.render(f'{self.game.score}', False, (64, 64, 64))
        self.rect = self.image.get_rect(midright = (780, 20))

    def update(self):
        self.image = self.font.render(f'{self.game.score}', False, (64, 64, 64))
        self.rect = self.image.get_rect(midright = (780, 20))

    def set_score(self, score):
        self.score = score
