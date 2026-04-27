import random
from pathlib import Path

import pygame

from .GameConfig import GameConfig
from .Monster import Monster
from .SnailExplosion import SnailExplosion

_ASSET_DIR = Path(__file__).resolve().parent.parent.parent.parent / "assets"
_IMAGE_PATH = _ASSET_DIR / "graphics" / "snail"

class Snail(Monster):

    _explosion_sound = None

    @property
    def explosion_sound(self):
        if Snail._explosion_sound is None:
            Snail._explosion_sound = pygame.mixer.Sound(str(_ASSET_DIR / 'audio' / 'explosion.wav'))
            Snail._explosion_sound.set_volume(1.0)
        return Snail._explosion_sound

    def __init__(self):
        super().__init__([str(_IMAGE_PATH / 'snail1.png'), str(_IMAGE_PATH / 'snail2.png')],
                         (random.randint(900, 1100), GameConfig.GROUND_LEVEL))

        self.damage_cooldown = 750
        self.damage_time = -1
        self.explosion = None
        self.explosion_damage_cooldown = 1000
        self.explosion_damage_time = -1

    def can_do_damage(self, current_time):
        return current_time - self.damage_time > self.damage_cooldown

    def set_damage_time(self, current_time):
        self.damage_time = current_time

    def hit(self):
        """Replace snail with explosion animation."""
        self.explosion = SnailExplosion(self.rect.center)
        self.active = False
        self.explosion_sound.play()

    def update(self):
        # If hit, don't move the snail anymore
        if self.explosion:
            return

        if self.rect.right < 0:
            self.kill()
        self.rect.x -= 4
        self.update_animation()

    def is_explosion_complete(self):
        """Check if explosion animation has completed."""
        if self.explosion:
            return self.explosion.is_complete()
        return False

    def can_explosion_do_damage(self, current_time):
        """Check if explosion can do damage."""
        if not self.explosion:
            return False
        return current_time - self.explosion_damage_time > self.explosion_damage_cooldown

    def set_explosion_damage_time(self, current_time):
        """Set the time when explosion damage was last applied."""
        self.explosion_damage_time = current_time

    def should_draw_snail(self):
        """Check if the snail itself should be drawn (not when exploded)."""
        return not self.explosion
