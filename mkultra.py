from game.Alien import Alien
from game.GameConfig import GameConfig
import pygame
from pygame.sprite import GroupSingle

class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(GameConfig.SCREEN_DIMENSION)
        pygame.display.set_caption('MK Ultra')

        graph_path = 'graphics/'
        self.sky_surface = pygame.image.load(graph_path + 'Sky.png').convert_alpha()
        self.ground_surface = pygame.image.load(graph_path + 'ground.png').convert_alpha()

        self.alien = GroupSingle()
        self.alien.add(Alien())

    def run_game(self):
        print('Launching MK Ultra')

        clock = pygame.time.Clock()

        print('Entering game loop')
        keep_running = True
        while keep_running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                    keep_running = False
                else:
                    self.alien.sprite.process_event(event)


            self.screen.blit(self.sky_surface, (0, 0))
            self.screen.blit(self.ground_surface, (0, 300))

            self.alien.update()
            self.alien.draw(self.screen)

            pygame.display.update()
            clock.tick(GameConfig.FPS)

        print('Exited game loop, shutting down MK Ultra.')
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run_game()
