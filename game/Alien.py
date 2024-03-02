from .GameConfig import GameConfig
import pygame
from pygame.sprite import Sprite

IMAGE_PATH = 'graphics/Player/'

class Alien(Sprite):

    _alien_stand_surface = None
    _alien_walk1_surface = None
    _alien_walk2_surface = None
    _alien_jump_surface = None

    @property
    def alien_stand_surface(self):
        if Alien._alien_stand_surface is None:
            Alien._alien_stand_surface = pygame.image.load(IMAGE_PATH + 'player_stand.png').convert_alpha()
        return Alien._alien_stand_surface

    @property
    def alien_walk1_surface(self):
        if Alien._alien_walk1_surface is None:
            Alien._alien_walk1_surface = pygame.image.load(IMAGE_PATH + 'player_walk_1.png').convert_alpha()
        return Alien._alien_walk1_surface

    @property
    def alien_walk2_surface(self):
        if Alien._alien_walk2_surface is None:
            Alien._alien_walk2_surface = pygame.image.load(IMAGE_PATH + 'player_walk_2.png').convert_alpha()
        return Alien._alien_walk2_surface

    @property
    def alien_jump_surface(self):
        if Alien._alien_jump_surface is None:
            Alien._alien_jump_surface = pygame.image.load(IMAGE_PATH + 'player_jump.png').convert_alpha()
        return Alien._alien_jump_surface

    def __init__(self):
        super().__init__()

        self.dx, self.dy = 0, 0

        self.alien_walk_surfaces = [self.alien_walk1_surface, self.alien_walk2_surface]
        self.walk_animation_idx = 0

        self.image = self.alien_stand_surface
        self.rect = self.image.get_rect(midbottom = (200, 300))

        self.keydown_a, self.keydown_d = False, False

        self.max_life_energy = 100
        self.life_energy = self.max_life_energy

        self.jump_sound = pygame.mixer.Sound('audio/cjump.mp3')
        self.jump_sound.set_volume(0.5)

    def update(self):
        # select character animation image
        if (self.dx, self.dy) == (0, 0):
            self.image = self.alien_stand_surface
        elif self.dy != 0:
            self.image = self.alien_jump_surface
        else:
            self.image = self.alien_walk_surfaces[int(self.walk_animation_idx)]

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

        self.walk_animation_idx = (self.walk_animation_idx + 0.1) % 2

    def process_event(self, event):
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
