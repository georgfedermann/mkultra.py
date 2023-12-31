from game.Alien import Alien
from game.Fly import Fly
from game.GameConfig import GameConfig
from game.Snail import Snail
import pygame
from pygame.joystick import Joystick
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
        self.font = pygame.font.Font('font/Pixeltype.ttf', 50)

        self.alien = GroupSingle()
        self.alien.add(Alien())

        self.fly_group = Group()
        self.snail_group = Group()

        self.clock = pygame.time.Clock()
        self.critter_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.critter_timer, 1500)

        self.keep_running = True
        self.mode = 'menu'

    def add_critter(self):
        if random.randint(0,10) >= 4:
            self.fly_group.add(Fly())
        else:
            self.snail_group.add(Snail())

    def run_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                self.keep_running = False
            elif event.type == self.critter_timer:
                self.add_critter()
            else:
                self.alien.sprite.process_event(event)

        self.screen.blit(self.sky_surface, (0, 0))
        self.screen.blit(self.ground_surface, (0, 300))

        self.alien.update()
        self.alien.draw(self.screen)

        self.fly_group.update()
        self.fly_group.draw(self.screen)
        self.snail_group.update()
        self.snail_group.draw(self.screen)

    def show_menu(self):
        self.screen.fill(GameConfig.MENU_BACKGROUND_COLOR)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or ( event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                self.keep_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.mode = 'game'
            elif event.type == pygame.JOYDEVICEADDED:
                print('Joystick added')
                self.joystick = Joystick(event.device_index)
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 2:
                    self.mode = 'game'

        label_mkultra_surface = self.font.render('MK Ultra', False, GameConfig.MENU_TITLE_COLOR)
        label_mkultra_rect = label_mkultra_surface.get_rect(midbottom = (GameConfig.SCREEN_WIDTH / 2, 80))
        label_run_surface = self.font.render('Press <Space> to run', False, GameConfig.MENU_TITLE_COLOR)
        label_run_rect = label_run_surface.get_rect(midbottom = (GameConfig.SCREEN_WIDTH / 2, 350))
        label_score_surface = self.font.render(f'{100}', True, (255, 196, 0))
        label_score_surface = pygame.transform.rotozoom(label_score_surface, 45, 1)
        label_score_rect = label_score_surface.get_rect(center = (600, 200))
        mkultra_label = pygame.transform.scale_by(pygame.image.load('graphics/Player/player_stand.png').convert_alpha(), 2)
        self.screen.blit(label_mkultra_surface, label_mkultra_rect)
        self.screen.blit(label_run_surface, label_run_rect)
        self.screen.blit(label_score_surface, label_score_rect)
        self.screen.blit(mkultra_label, mkultra_label.get_rect(center = (GameConfig.SCREEN_WIDTH / 2, GameConfig.SCREEN_HEIGHT / 2)))

    def run_mkultra(self):
        print('Launching MK Ultra')

        print('Entering game loop')

        while self.keep_running:

            if self.mode == 'menu':
                self.show_menu()
            elif self.mode == 'game':
                self.run_game()

            pygame.display.update()
            self.clock.tick(GameConfig.FPS)

        print('Exited game loop, shutting down MK Ultra.')
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run_mkultra()
