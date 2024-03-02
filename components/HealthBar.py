import pygame
from pygame.sprite import Sprite

class HealthBar(Sprite):
    """
    Basically visualizes the remaining percentage of a KPI, e.g. the remaining health of a player.
    """

    OUTER_WIDTH = 400
    OUTER_HEIGHT = 50

    INNER_WIDTH = 384
    INNER_HEIGHT = 30

    INNER_ORIGIN = (9, 10)

    DARK_GREEN = (0, 100, 0)
    GREEN = (0, 255, 0)
    WHITE = (255, 255, 255)

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

        self.image = pygame.Surface((HealthBar.OUTER_WIDTH, HealthBar.OUTER_HEIGHT))
        self.rect = self.image.get_rect(topleft = position)

        self.background = pygame.image.load("graphics/healthbar//background.png").convert_alpha()

        self.dirty = True

    def update(self) -> None:
        if self.dirty:
            print('Re-render health bar')
            self.image.blit(self.background, (0, 0))

            health_bar_background = pygame.Rect(HealthBar.INNER_ORIGIN, (HealthBar.INNER_WIDTH, HealthBar.INNER_HEIGHT))
            pygame.draw.rect(self.image, HealthBar.DARK_GREEN, health_bar_background)

            current_health_width = HealthBar.INNER_WIDTH * self.percentage
            health_bar = pygame.Rect(HealthBar.INNER_ORIGIN, (current_health_width, HealthBar.INNER_HEIGHT))
            pygame.draw.rect(self.image, HealthBar.GREEN, health_bar)

            # Add glossy effect
            for i in range(HealthBar.INNER_HEIGHT // 2):
                alpha = 220 - ( i * (120 // (HealthBar.INNER_HEIGHT // 2)))
                glossy_effect = pygame.Surface((current_health_width, 1))
                glossy_effect.set_alpha(alpha)
                glossy_effect.fill(HealthBar.WHITE)
                self.image.blit(glossy_effect, (HealthBar.INNER_ORIGIN[0], HealthBar.INNER_ORIGIN[1] + i))

            line = pygame.Surface((current_health_width, 2))
            line.fill(HealthBar.WHITE)
            self.image.blit(line, (HealthBar.INNER_ORIGIN[0], HealthBar.INNER_ORIGIN[1] + HealthBar.INNER_HEIGHT // 3))
            self.dirty = False

    def set_percentage(self, percentage: float) -> None:
        """
        Set the percentage value.
        Args:
            percentage (float): A float between 0 and 1 indicating the percentage of the KPI.
        """
        assert 0 <= percentage <= 1, "Percentage must be a value between 0 and 1 but was " + str(percentage)
        self.percentage = percentage
        self.dirty = True
