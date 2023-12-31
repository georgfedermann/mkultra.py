from game.Alien import Alien
from game.Fly import Fly
from game.GameConfig import GameConfig
import pygame
from pygame.sprite import Group,  GroupSingle
import random

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

        self.fly_group = Group()

    def add_critter(self):
        if random.randint(0,10) >= 4:
            self.fly_group.add(Fly())


    def run_game(self):
        print('Launching MK Ultra')

        clock = pygame.time.Clock()
        critter_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(critter_timer, 1500)

        print('Entering game loop')
        keep_running = True
        while keep_running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                    keep_running = False
                elif event.type == critter_timer:
                    self.add_critter()
                else:
                    self.alien.sprite.process_event(event)


            self.screen.blit(self.sky_surface, (0, 0))
            self.screen.blit(self.ground_surface, (0, 300))

            self.alien.update()
            self.alien.draw(self.screen)

            self.fly_group.update()
            self.fly_group.draw(self.screen)

            pygame.display.update()
            clock.tick(GameConfig.FPS)

        print('Exited game loop, shutting down MK Ultra.')
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run_game()
