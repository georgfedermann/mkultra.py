import pygame
from pygame.sprite import Sprite

from mkultra.assets import load_font


class ScoreBoard(Sprite):

    WIDTH = 200
    HEIGHT = 44
    POSITION = (590, 8)
    PULSE_DURATION_MS = 520

    BACKGROUND = (12, 16, 24)
    PANEL = (30, 36, 46)
    FRAME = (158, 190, 210)
    FRAME_DARK = (59, 72, 86)
    CYAN = (70, 238, 255)
    GOLD = (255, 202, 57)
    RED = (255, 50, 26)
    WHITE = (246, 252, 255)

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.font = load_font('font/Pixeltype.ttf', 30)
        self.label_font = load_font('font/Pixeltype.ttf', 20)
        self.score = self.game.score
        self.highlight_until = 0
        self.highlight_level = 0
        self.image = pygame.Surface((ScoreBoard.WIDTH, ScoreBoard.HEIGHT), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft = ScoreBoard.POSITION)
        self.dirty = True

    def update(self):
        if self.score != self.game.score:
            self.set_score(self.game.score)

        if self.dirty or pygame.time.get_ticks() < self.highlight_until:
            self._render()
            self.dirty = False

    def set_score(self, score):
        self.score = score
        self.dirty = True

    def flash(self, level=1):
        self.highlight_level = level
        self.highlight_until = pygame.time.get_ticks() + ScoreBoard.PULSE_DURATION_MS
        self.dirty = True

    def _render(self):
        self.image.fill((0, 0, 0, 0))
        pulse = self._pulse()
        glow_color = ScoreBoard.GOLD if self.highlight_level >= 2 else ScoreBoard.CYAN

        self._draw_frame(glow_color, pulse)
        self._draw_score(glow_color, pulse)
        self._draw_meter(glow_color, pulse)

    def _draw_frame(self, glow_color, pulse):
        frame_points = [
            (8, 0),
            (ScoreBoard.WIDTH - 16, 0),
            (ScoreBoard.WIDTH, 12),
            (ScoreBoard.WIDTH - 8, ScoreBoard.HEIGHT),
            (14, ScoreBoard.HEIGHT),
            (0, ScoreBoard.HEIGHT - 10),
        ]
        pygame.draw.polygon(self.image, ScoreBoard.PANEL, frame_points)
        pygame.draw.lines(self.image, ScoreBoard.FRAME, True, frame_points, 2)

        inner = pygame.Rect(10, 8, ScoreBoard.WIDTH - 20, ScoreBoard.HEIGHT - 16)
        pygame.draw.rect(self.image, ScoreBoard.BACKGROUND, inner)
        pygame.draw.rect(self.image, ScoreBoard.FRAME_DARK, inner, 1)

        if pulse:
            glow = pygame.Surface((ScoreBoard.WIDTH, ScoreBoard.HEIGHT), pygame.SRCALPHA)
            pygame.draw.lines(glow, (*glow_color, int(155 * pulse)), True, frame_points, 4)
            self.image.blit(glow, (0, 0))

    def _draw_score(self, glow_color, pulse):
        label = self.label_font.render('SCORE', False, ScoreBoard.CYAN)
        self.image.blit(label, (18, 4))

        score_text = f'{self.score:06}'
        score_color = ScoreBoard.WHITE
        if pulse:
            score_color = glow_color
        score_surface = self.font.render(score_text, False, score_color)
        score_rect = score_surface.get_rect(midright = (ScoreBoard.WIDTH - 18, 26))
        self.image.blit(score_surface, score_rect)

        if pulse:
            flare = pygame.Surface(score_rect.size, pygame.SRCALPHA)
            flare.fill((*glow_color, int(55 * pulse)))
            self.image.blit(flare, score_rect)

    def _draw_meter(self, glow_color, pulse):
        segment_width = 12
        segment_gap = 4
        filled_segments = (self.score // 100) % 10
        y = ScoreBoard.HEIGHT - 8
        for segment in range(10):
            x = 18 + segment * (segment_width + segment_gap)
            color = ScoreBoard.FRAME_DARK
            if segment < filled_segments:
                color = glow_color if pulse else ScoreBoard.GOLD
            pygame.draw.rect(self.image, color, (x, y, segment_width, 3))

        warning_color = ScoreBoard.RED if self.highlight_level >= 2 and pulse else ScoreBoard.FRAME_DARK
        pygame.draw.circle(self.image, warning_color, (ScoreBoard.WIDTH - 10, 9), 4)

    def _pulse(self):
        remaining = self.highlight_until - pygame.time.get_ticks()
        if remaining <= 0:
            self.highlight_level = 0
            return 0
        return remaining / ScoreBoard.PULSE_DURATION_MS
