import random

import pygame

from mkultra.assets import load_sound

from .GameConfig import GameConfig
from .Monster import Monster
from .SnailExplosion import SnailExplosion


class Snail(Monster):

    _explosion_sound = None
    _punch_sound = None
    ARROW_WIDTH = 18
    ARROW_HEIGHT = 20

    @property
    def explosion_sound(self):
        if Snail._explosion_sound is None:
            Snail._explosion_sound = load_sound('audio/explosion.wav')
            Snail._explosion_sound.set_volume(1.0)
        return Snail._explosion_sound

    @property
    def punch_sound(self):
        if Snail._punch_sound is None:
            Snail._punch_sound = load_sound('audio/punch.mp3')
            Snail._punch_sound.set_volume(0.5)
        return Snail._punch_sound

    def __init__(self, can_be_stomped=False, start_x=None):
        if start_x is None:
            start_x = random.randint(GameConfig.SPAWN_X_MIN, GameConfig.SPAWN_X_MAX)

        super().__init__(['graphics/snail/snail1.png', 'graphics/snail/snail2.png'],
                         (start_x, GameConfig.GROUND_LEVEL))

        self.can_be_stomped = can_be_stomped
        self.arrow_tick = 0
        self.dy = 0
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

    def stomp(self):
        self.active = False
        self.dy = 0
        self.image = pygame.transform.rotozoom(self.image, 180, 1)
        self.punch_sound.play()

    def weak_spot_centerx(self):
        return self.rect.centerx

    def is_hit_in_weak_spot(self, player):
        if not self.can_be_stomped:
            return False

        vertical_overlap = player.rect.bottom - self.rect.top
        max_stomp_depth = max(12, player.dy + 4)
        weak_spot_distance = abs(player.rect.centerx - self.weak_spot_centerx())
        return player.dy >= 0 and 0 <= vertical_overlap <= max_stomp_depth and weak_spot_distance <= GameConfig.SNAIL_WEAK_SPOT_MARGIN

    def update(self):
        # If hit, don't move the snail anymore
        if self.explosion:
            return

        if self.rect.right < 0 or self.rect.top > GameConfig.SCREEN_HEIGHT:
            self.kill()
        if self.active:
            self.rect.x -= 4
            self.arrow_tick = (self.arrow_tick + 1) % 60
            self.update_animation()
        else:
            self.rect.y += self.dy
            self.dy += 1

    def draw_marker(self, screen, camera=None):
        if not self.can_be_stomped or not self.active or self.explosion:
            return

        pulse = abs(30 - self.arrow_tick) / 30
        arrow_y = self.rect.top - 28 + int(8 * pulse)
        arrow_x = self.weak_spot_centerx()
        if camera:
            arrow_x -= camera.offset_x
        glow_color = (255, 250, 100) if self.arrow_tick % 12 < 6 else (255, 68, 24)
        core_color = (255, 255, 255)

        arrow_points = [
            (arrow_x, arrow_y + Snail.ARROW_HEIGHT),
            (arrow_x - Snail.ARROW_WIDTH // 2, arrow_y + 7),
            (arrow_x - 4, arrow_y + 7),
            (arrow_x - 4, arrow_y),
            (arrow_x + 4, arrow_y),
            (arrow_x + 4, arrow_y + 7),
            (arrow_x + Snail.ARROW_WIDTH // 2, arrow_y + 7),
        ]
        pygame.draw.polygon(screen, glow_color, arrow_points)
        pygame.draw.lines(screen, (35, 12, 4), True, arrow_points, 2)
        pygame.draw.line(screen, core_color, (arrow_x, arrow_y + 2), (arrow_x, arrow_y + Snail.ARROW_HEIGHT - 4), 2)

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
