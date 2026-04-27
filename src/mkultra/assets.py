from functools import lru_cache
from pathlib import Path

import pygame

ASSET_ROOT = Path(__file__).resolve().parents[2] / "assets"


def asset_path(*parts: str) -> Path:
    """Return an absolute path inside the project asset directory."""
    return ASSET_ROOT.joinpath(*parts)


@lru_cache
def load_image(relative_path: str) -> pygame.Surface:
    """Load and cache an image surface from the asset directory."""
    return pygame.image.load(str(asset_path(relative_path))).convert_alpha()


@lru_cache
def load_sound(relative_path: str) -> pygame.mixer.Sound:
    """Load and cache a sound from the asset directory."""
    return pygame.mixer.Sound(str(asset_path(relative_path)))


@lru_cache
def load_font(relative_path: str, size: int) -> pygame.font.Font:
    """Load and cache a font from the asset directory."""
    return pygame.font.Font(str(asset_path(relative_path)), size)
