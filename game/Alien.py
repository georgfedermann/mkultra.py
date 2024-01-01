from .GameConfig import GameConfig
import pygame
from pygame.sprite import Sprite

IMAGE_PATH = 'graphics/Player/'

class Alien(Sprite):

    def __init__(self):
        super().__init__()

        self.dx, self.dy = 0, 0

        self.alien_stand_surface = pygame.image.load(IMAGE_PATH + 'player_stand.png').convert_alpha()
        self.alien_walk1_surface = pygame.image.load(IMAGE_PATH + 'player_walk_1.png').convert_alpha()
        self.alien_walk2_surface = pygame.image.load(IMAGE_PATH + 'player_walk_2.png').convert_alpha()
        self.alien_jump_surface = pygame.image.load(IMAGE_PATH + 'player_jump.png').convert_alpha()
        self.alien_walk_surfaces = [self.alien_walk1_surface, self.alien_walk2_surface]
        self.walk_animation_idx = 0

        self.image = self.alien_stand_surface
        self.rect = self.image.get_rect(midbottom = (200, 300))

        self.keydown_a, self.keydown_d = False, False

        self.life_energy = 100

        self.jump_sound = pygame.mixer.Sound('audio/cjump.mp3')
        self.jump_sound.set_volume(0.5)

    def update(self):
        if (self.dx, self.dy) == (0, 0):
            self.image = self.alien_stand_surface
        elif self.dy != 0:
            self.image = self.alien_jump_surface
        else:
            self.image = self.alien_walk_surfaces[int(self.walk_animation_idx)]

        self.rect.x += self.dx * GameConfig.MOVE_SCALE

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
