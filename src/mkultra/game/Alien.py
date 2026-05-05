import pygame
from pygame.sprite import Sprite

from mkultra.assets import load_image, load_sound

from .GameConfig import GameConfig


class Alien(Sprite):

    _alien_stand_surface = None
    _alien_walk1_surface = None
    _alien_walk2_surface = None
    _alien_jump_surface = None

    @property
    def alien_stand_surface(self):
        if Alien._alien_stand_surface is None:
            Alien._alien_stand_surface = load_image('graphics/Player/player_stand.png')
        return Alien._alien_stand_surface

    @property
    def alien_walk1_surface(self):
        if Alien._alien_walk1_surface is None:
            Alien._alien_walk1_surface = load_image('graphics/Player/player_walk_1.png')
        return Alien._alien_walk1_surface

    @property
    def alien_walk2_surface(self):
        if Alien._alien_walk2_surface is None:
            Alien._alien_walk2_surface = load_image('graphics/Player/player_walk_2.png')
        return Alien._alien_walk2_surface

    @property
    def alien_jump_surface(self):
        if Alien._alien_jump_surface is None:
            Alien._alien_jump_surface = load_image('graphics/Player/player_jump.png')
        return Alien._alien_jump_surface

    def __init__(self):
        super().__init__()

        self.dx, self.dy = 0, 0

        self.alien_walk_surfaces = [self.alien_walk1_surface, self.alien_walk2_surface]
        self.walk_animation_idx = 0

        self.image = self.alien_stand_surface
        self.rect = self.image.get_rect(midbottom = (200, 300))
        self.base_image = self.image

        self.keydown_a, self.keydown_d = False, False
        self.dying = False
        self.death_started_at = 0
        self.death_origin_x = self.rect.centerx

        self.max_life_energy = 100
        self.life_energy = self.max_life_energy

        self.jump_sound = load_sound('audio/cjump.mp3')
        self.jump_sound.set_volume(0.5)

    def apply_damage(self, damage):
        assert self.life_energy >= 0, f"life_energy must be >= 0 but was {self.life_energy}"
        assert damage >= 0, f"damage must be >= 0 but was {damage}"
        self.life_energy -= min(self.life_energy, damage)

    def update(self):
        if self.dying:
            self.update_death_animation()
            return

        # select character animation image
        if (self.dx, self.dy) == (0, 0):
            self.image = self.alien_stand_surface
        elif self.dy != 0:
            self.image = self.alien_jump_surface
        else:
            self.image = self.alien_walk_surfaces[int(self.walk_animation_idx)]
        self.base_image = self.image

        # handle character movement
        if self.dx > 0:
            self.rect.x += min(self.dx * GameConfig.MOVE_SCALE, GameConfig.SCREEN_WIDTH - self.rect.right)
        elif self.dx < 0:
            self.rect.x += max(self.dx * GameConfig.MOVE_SCALE, -self.rect.left)

        if self.rect.bottom < GameConfig.GROUND_LEVEL or self.dy < 0:
            self.rect.bottom = min(self.rect.bottom + self.dy, GameConfig.GROUND_LEVEL)
            self.dy += 1
            if self.rect.bottom == GameConfig.GROUND_LEVEL:
                self.image = self.alien_stand_surface
                self.dy = 0

        self.walk_animation_idx = (self.walk_animation_idx + GameConfig.ANIMATION_SPEED) % 2

    def start_death_animation(self):
        self.dying = True
        self.dx = 0
        self.dy = 0
        self.death_started_at = pygame.time.get_ticks()
        self.death_origin_x = self.rect.centerx
        self.base_image = self.image

    def update_death_animation(self):
        progress = min(1, (pygame.time.get_ticks() - self.death_started_at) / GameConfig.DEATH_ANIMATION_DURATION_MS)
        alpha = max(0, int(255 * (1 - progress)))
        wobble = int(GameConfig.DEATH_WOBBLE_AMPLITUDE * pygame.math.Vector2(1, 0).rotate(progress * 1440).x)

        self.rect.centerx = self.death_origin_x + wobble
        self.rect.y -= GameConfig.DEATH_FLOAT_SPEED
        self.image = self.base_image.copy()
        self.image.set_alpha(alpha)

    def is_death_animation_complete(self):
        elapsed = pygame.time.get_ticks() - self.death_started_at
        return self.dying and (elapsed >= GameConfig.DEATH_ANIMATION_DURATION_MS or self.rect.bottom < 0)

    def process_event(self, event):
        if self.dying:
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.keydown_a = True
                self.dx = -1
            elif event.key == pygame.K_d:
                self.keydown_d = True
                self.dx = 1
            elif (event.key == pygame.K_SPACE or event.key == pygame.K_w) and self.rect.bottom == GameConfig.GROUND_LEVEL:
                self.dy = GameConfig.JUMP_IMPULSE
                self.jump_sound.play()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                self.keydown_a = False
                if not self.keydown_d:
                    self.dx = 0
            elif event.key == pygame.K_d:
                self.keydown_d = False
                if not self.keydown_a:
                    self.dx = 0
        elif event.type == pygame.JOYBUTTONDOWN:
            if event.button == 1 and self.rect.bottom == GameConfig.GROUND_LEVEL:
                self.dy = GameConfig.JUMP_IMPULSE
                self.jump_sound.play()
        elif event.type == pygame.JOYAXISMOTION:
            if event.axis == 0:
                self.dx = event.value
