import pygame
from pygame.sprite import Sprite


class HealthBar(Sprite):
    """
    Basically visualizes the remaining percentage of a KPI, e.g. the remaining health of a player.
    """

    OUTER_WIDTH = 300
    OUTER_HEIGHT = 38

    INNER_WIDTH = 226
    INNER_HEIGHT = 16

    INNER_ORIGIN = (52, 11)

    # will start blinking and sound an alarm when the percentage drops below this threshold
    CRITICAL_THRESHOLD = 0.18
    BLINK_INTERVAL_MS = 180

    BLACK = (5, 7, 10)
    FRAME_DARK = (26, 31, 38)
    FRAME_LIGHT = (95, 107, 121)
    FRAME_HIGHLIGHT = (178, 195, 209)
    SLOT_DARK = (16, 10, 8)
    SLOT_RED = (70, 5, 3)
    GREEN = (0, 232, 96)
    ORANGE = (255, 130, 18)
    RED = (255, 34, 18)
    WHITE = (255, 255, 255)
    WARNING_YELLOW = (255, 214, 43)
    WARNING_RED = (255, 24, 12)

    def __init__(self, position, percentage):
        """
        Creates a Healthbar widget.
        Args:
            position (tuple): A tuple containing the x and y coordinates of the top left corner of the widget.
            percentage (float): A float between 0 and 1 indicating the percentage of the KPI.
        """
        super().__init__()
        assert 0 <= percentage <= 1, "Percentage must be a value between 0 and 1."

        self.percentage = percentage
        self.position = position

        self.image = pygame.Surface((HealthBar.OUTER_WIDTH, HealthBar.OUTER_HEIGHT), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft = position)

        self.dirty = True
        self.blink_visible = True

    def update(self) -> None:
        blink_visible = True
        if self.percentage <= HealthBar.CRITICAL_THRESHOLD:
            blink_visible = (pygame.time.get_ticks() // HealthBar.BLINK_INTERVAL_MS) % 2 == 0

        if self.dirty or blink_visible != self.blink_visible:
            self.blink_visible = blink_visible
            self._render()
            self.dirty = False

    def _render(self) -> None:
        self.image.fill((0, 0, 0, 0))
        self._draw_frame()
        self._draw_warning_lamps()
        self._draw_energy_slot()

        if self.percentage > HealthBar.CRITICAL_THRESHOLD or self.blink_visible:
            self._draw_energy_fill()

        self._draw_armor_lines()

    def _draw_frame(self) -> None:
        outer = pygame.Rect(0, 0, HealthBar.OUTER_WIDTH, HealthBar.OUTER_HEIGHT)
        frame_points = [
            (10, 0),
            (HealthBar.OUTER_WIDTH - 18, 0),
            (HealthBar.OUTER_WIDTH, 12),
            (HealthBar.OUTER_WIDTH - 9, HealthBar.OUTER_HEIGHT),
            (18, HealthBar.OUTER_HEIGHT),
            (0, HealthBar.OUTER_HEIGHT - 11),
        ]
        pygame.draw.polygon(self.image, HealthBar.FRAME_DARK, frame_points)
        pygame.draw.lines(self.image, HealthBar.FRAME_HIGHLIGHT, True, frame_points, 2)
        pygame.draw.rect(self.image, HealthBar.BLACK, outer.inflate(-12, -10), 1)

    def _draw_warning_lamps(self) -> None:
        critical_visible = self.percentage <= HealthBar.CRITICAL_THRESHOLD and self.blink_visible
        lamp_color = HealthBar.WARNING_RED if critical_visible else HealthBar.WARNING_YELLOW
        status_light = HealthBar.RED if self.percentage <= HealthBar.CRITICAL_THRESHOLD else HealthBar.FRAME_LIGHT

        pygame.draw.polygon(self.image, lamp_color, [(13, 8), (38, 8), (44, 19), (38, 30), (13, 30), (7, 19)])
        pygame.draw.polygon(self.image, HealthBar.BLACK, [(25, 12), (34, 19), (25, 26), (27, 21), (16, 21), (25, 12)])
        pygame.draw.circle(self.image, status_light, (289, 19), 5)

    def _draw_energy_slot(self) -> None:
        slot = pygame.Rect(HealthBar.INNER_ORIGIN, (HealthBar.INNER_WIDTH, HealthBar.INNER_HEIGHT))
        pygame.draw.rect(self.image, HealthBar.SLOT_RED, slot)
        pygame.draw.rect(self.image, HealthBar.SLOT_DARK, slot.inflate(-4, -4))
        pygame.draw.rect(self.image, HealthBar.FRAME_LIGHT, slot, 2)

        for x in range(slot.left + 18, slot.right, 28):
            pygame.draw.line(self.image, HealthBar.BLACK, (x, slot.top + 2), (x - 5, slot.bottom - 3), 2)

    def _draw_energy_fill(self) -> None:
        current_width = int(HealthBar.INNER_WIDTH * self.percentage)
        if current_width <= 0:
            return

        fill_rect = pygame.Rect(HealthBar.INNER_ORIGIN, (current_width, HealthBar.INNER_HEIGHT))
        pygame.draw.rect(self.image, self._energy_color(), fill_rect.inflate(-4, -4))
        pygame.draw.line(self.image, HealthBar.WHITE, (fill_rect.left + 5, fill_rect.top + 4), (fill_rect.right - 5, fill_rect.top + 4), 1)
        pygame.draw.line(
            self.image,
            HealthBar.BLACK,
            (fill_rect.left + 4, fill_rect.bottom - 5),
            (fill_rect.right - 4, fill_rect.bottom - 5),
            1,
        )

    def _draw_armor_lines(self) -> None:
        pygame.draw.line(self.image, HealthBar.FRAME_LIGHT, (54, 5), (266, 5), 1)
        pygame.draw.line(self.image, HealthBar.FRAME_LIGHT, (59, 33), (259, 33), 1)
        pygame.draw.line(self.image, HealthBar.FRAME_HIGHLIGHT, (282, 8), (294, 19), 2)
        pygame.draw.line(self.image, HealthBar.FRAME_HIGHLIGHT, (293, 19), (283, 30), 2)

    def _energy_color(self) -> tuple[int, int, int]:
        if self.percentage > 0.5:
            return self._lerp_color(HealthBar.ORANGE, HealthBar.GREEN, (self.percentage - 0.5) / 0.5)
        return self._lerp_color(HealthBar.RED, HealthBar.ORANGE, self.percentage / 0.5)

    def _lerp_color(self, low_color: tuple[int, int, int], high_color: tuple[int, int, int], factor: float) -> tuple[int, int, int]:
        factor = max(0, min(1, factor))
        return tuple(int(low_color[index] + (high_color[index] - low_color[index]) * factor) for index in range(3))

    def set_percentage(self, percentage: float) -> None:
        """
        Set the percentage value.
        Args:
            percentage (float): A float between 0 and 1 indicating the percentage of the KPI.
        """
        assert 0 <= percentage <= 1, "Percentage must be a value between 0 and 1 but was " + str(percentage)
        self.percentage = percentage
        self.dirty = True
