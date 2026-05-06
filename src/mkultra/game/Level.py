from pygame.sprite import Group

from mkultra.assets import load_image

from .Camera import Camera
from .GameConfig import GameConfig
from .Platform import Platform


class Level:
    def __init__(self):
        self.width = GameConfig.LEVEL_WIDTH
        self.camera = Camera(self.width)
        self.sky_surface = load_image('graphics/Sky.png')
        self.ground_surface = load_image('graphics/ground.png')
        self.platforms = Group()
        self.build_platforms()

    def build_platforms(self):
        # Placeholder geometry for future level design; ground keeps current gameplay intact.
        self.platforms.add(
            Platform(
                (0, GameConfig.GROUND_LEVEL, self.width, GameConfig.SCREEN_HEIGHT - GameConfig.GROUND_LEVEL),
                visible=False,
            )
        )

    def add_static_platform(self, rect):
        platform = Platform(rect)
        self.platforms.add(platform)
        return platform

    def add_moving_platform(self, rect, velocity, movement_bounds):
        platform = Platform(rect, velocity=velocity, movement_bounds=movement_bounds)
        self.platforms.add(platform)
        return platform

    def update(self, player_rect):
        self.camera.update(player_rect)
        self.platforms.update()

    def draw_background(self, screen):
        screen.blit(self.sky_surface, (0, 0))
        ground_width = self.ground_surface.get_width()
        start_x = -(self.camera.offset_x % ground_width)
        for x in range(start_x, GameConfig.SCREEN_WIDTH, ground_width):
            screen.blit(self.ground_surface, (x, GameConfig.GROUND_LEVEL))

    def draw_platforms(self, screen):
        visible_area = self.camera.visible_area()
        for platform in self.platforms.sprites():
            if not platform.visible:
                continue
            if platform.rect.colliderect(visible_area):
                screen.blit(platform.image, self.camera.apply_rect(platform.rect))

    def ground_level_for(self, rect):
        floor = GameConfig.GROUND_LEVEL
        for platform in self.platforms.sprites():
            if rect.right <= platform.rect.left or rect.left >= platform.rect.right:
                continue
            if rect.bottom <= platform.rect.top:
                floor = min(floor, platform.rect.top)
        return floor

    def clamp_horizontal_movement(self, rect, delta_x):
        if delta_x > 0:
            return min(delta_x, self.width - rect.right)
        if delta_x < 0:
            return max(delta_x, -rect.left)
        return 0
