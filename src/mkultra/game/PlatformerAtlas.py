from functools import lru_cache

import pygame

from mkultra.assets import asset_path

from .GameConfig import GameConfig


class PlatformerAtlas:
    SPRITESHEET_PATH = 'graphics/platformer/spritesheet.png'
    BACKGROUNDS_PATH = 'graphics/platformer/backgrounds.png'
    COLOR_KEY = (94, 129, 162)
    PLAYER_Y = 3
    PLAYER_WIDTH = 22
    PLAYER_HEIGHT = 21

    RECTS = {
        'player_stand': pygame.Rect(440, PLAYER_Y, PLAYER_WIDTH, PLAYER_HEIGHT),
        'player_dance': pygame.Rect(484, PLAYER_Y, PLAYER_WIDTH, PLAYER_HEIGHT),
        'player_death': pygame.Rect(531, PLAYER_Y, PLAYER_WIDTH, PLAYER_HEIGHT),
        'player_climb_1': pygame.Rect(554, PLAYER_Y, PLAYER_WIDTH, PLAYER_HEIGHT),
        'player_climb_2': pygame.Rect(577, PLAYER_Y, PLAYER_WIDTH, PLAYER_HEIGHT),
        'player_walk_1': pygame.Rect(646, PLAYER_Y, PLAYER_WIDTH, PLAYER_HEIGHT),
        'player_walk_2': pygame.Rect(668, PLAYER_Y, PLAYER_WIDTH, PLAYER_HEIGHT),
        'fly_1': pygame.Rect(300, 328, 22, 20),
        'fly_2': pygame.Rect(324, 328, 22, 20),
        'coin': pygame.Rect(416, 50, 22, 20),
        'heart_full': pygame.Rect(436, 95, 22, 20),
        'heart_empty': pygame.Rect(484, 95, 22, 20),
        'terrain_grass_left': pygame.Rect(26, 72, 21, 21),
        'terrain_grass_center': pygame.Rect(49, 72, 21, 21),
        'terrain_grass_right': pygame.Rect(72, 72, 21, 21),
        'terrain_dirt_center': pygame.Rect(49, 95, 21, 21),
    }

    def __init__(self, scale=GameConfig.PLATFORMER_ASSET_SCALE):
        self.scale = scale
        self.spritesheet = self.load_sheet(self.SPRITESHEET_PATH)
        self.backgrounds = self.load_sheet(self.BACKGROUNDS_PATH)
        self._cache = {}

    def load_sheet(self, relative_path):
        surface = pygame.image.load(str(asset_path(relative_path)))
        if pygame.display.get_surface():
            return surface.convert()
        return surface

    def sprite(self, name, scale=None):
        if name not in self.RECTS:
            raise KeyError(f"Unknown platformer sprite: {name}")

        scale = self.scale if scale is None else scale
        cache_key = (name, scale)
        if cache_key not in self._cache:
            surface = self.spritesheet.subsurface(self.RECTS[name]).copy()
            surface.set_colorkey(self.COLOR_KEY)
            if scale != 1:
                surface = pygame.transform.scale_by(surface, scale)
            self._cache[cache_key] = surface
        return self._cache[cache_key]

    def tile(self, name):
        return self.sprite(name)

    def background(self, scale=GameConfig.PLATFORMER_ASSET_SCALE):
        cache_key = ('background', scale)
        if cache_key not in self._cache:
            surface = self.backgrounds.copy()
            if scale != 1:
                surface = pygame.transform.scale_by(surface, scale)
            self._cache[cache_key] = surface
        return self._cache[cache_key]


@lru_cache
def platformer_atlas():
    return PlatformerAtlas()
