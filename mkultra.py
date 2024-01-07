from game.Alien import Alien
from components.HealthBar import HealthBar
from game.Fly import Fly
from game.GameConfig import GameConfig
from game.ScoreBoard import ScoreBoard
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

        self.score = 0
        self.score_board = ScoreBoard(self)
        self.score_board.set_score(self.score)

        self.alien = GroupSingle()
        self.alien.add(Alien())
        self.health_bar = HealthBar((10, 10), self.alien.sprite.life_energy / self.alien.sprite.max_life_energy)

        self.fly_group = Group()
        self.snail_group = Group()
        self.dead_critter_group = Group()
        self.dead_critter_group.add(self.health_bar)
        self.dead_critter_group.add(self.score_board)

        self.clock = pygame.time.Clock()
        self.critter_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.critter_timer, 1500)

        self.keep_running = True
        self.mode = 'splash'

        self.game_music = pygame.mixer.Sound('audio/music.wav')
        self.game_music.set_volume(0.2)

        self.intro_music = pygame.mixer.Sound('audio/intro.mp3')
        self.intro_music.set_volume(0.2)

        self.after_game_music = pygame.mixer.Sound('audio/hiscore.mp3')
        self.after_game_music.set_volume(0.2)
        self.achievement_sound = pygame.mixer.Sound('audio/achievement.mp3')

    def reset_game(self):
        print('Resetting game')
        self.alien.add(Alien())
        self.fly_group.empty()
        self.snail_group.empty()
        self.health_bar.set_percentage(self.alien.sprite.life_energy / self.alien.sprite.max_life_energy)
        self.score = 0
        self.score_board.set_score(self.score)
        print(f'dead_critter_group {len(self.dead_critter_group)}')
        # self.dead_critter_group.empty()
        self.score = 0

    def add_critter(self):
        if random.randint(0,10) >= 4:
            self.fly_group.add(Fly())
        else:
            self.snail_group.add(Snail())

    def check_collisions(self):
        # flies
        collision_flies = pygame.sprite.spritecollide(self.alien.sprite, self.fly_group, True)
        player = self.alien.sprite
        if collision_flies:
            hit_count = 0
            print(f"Collision with {len(collision_flies)} flies")

            for fly in collision_flies:
                delta_x = abs(player.rect.centerx - fly.rect.centerx)
                delta_y = abs(player.rect.bottom - fly.rect.top)
                print(f'delta x {delta_x}, delta_y {delta_y}')
                if delta_y < 6 and delta_x < 55:
                    self.dead_critter_group.add(fly)
                    self.score += GameConfig.FLY_SCORE
                    fly.hit()
                    hit_count += 1
                else:
                    self.fly_group.add(fly)
                    if fly.can_do_damage(pygame.time.get_ticks()):
                        fly.set_damage_time(pygame.time.get_ticks())
                        player.life_energy -= GameConfig.FLY_DAMAGE
                        if player.life_energy <= 0:
                            self.mode = 'hiscores'

            if hit_count > 1:
                self.achievement_sound.play()
                self.score += GameConfig.FLY_SCORE * hit_count
                self.alien.sprite.life_energy = self.alien.sprite.max_life_energy

        # snails
        snails = pygame.sprite.spritecollide(self.alien.sprite, self.snail_group, False)
        if snails:
            for snail in snails:
                if snail.can_do_damage(pygame.time.get_ticks()):
                    player.life_energy -= GameConfig.SNAIL_DAMAGE
                    snail.set_damage_time(pygame.time.get_ticks())
            if player.life_energy <= 0:
                self.mode = 'hiscores'

    def run_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                self.keep_running = False
            elif event.type == self.critter_timer:
                self.add_critter()
            elif event.type == pygame.KEYDOWN  and event.key == pygame.K_m:
                    if self.game_music.get_num_channels() == 0:
                        self.game_music.play(-1)
                    else:
                        self.game_music.stop()
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
        self.health_bar.set_percentage(self.alien.sprite.life_energy / self.alien.sprite.max_life_energy)
        self.dead_critter_group.update()
        self.dead_critter_group.draw(self.screen)

        self.check_collisions()

    def show_splash(self):
        self.game_music.stop()
        if self.intro_music.get_num_channels() == 0:
           self.intro_music.play(-1)
        self.screen.fill(GameConfig.MENU_BACKGROUND_COLOR)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or ( event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                self.keep_running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.reset_game()
                    self.mode = 'game'
                    self.intro_music.stop()
                    if self.game_music.get_num_channels() == 0:
                        self.game_music.play(-1)
            elif event.type == pygame.JOYDEVICEADDED:
                print('Joystick added')
                self.joystick = Joystick(event.device_index)
            elif event.type == pygame.JOYBUTTONDOWN:
                print(f'Joystick button {event.button} pressed')
                if event.button == 2:
                    print('Joystick button 2 pressed')
                    self.reset_game()
                    self.mode = 'game'
                    self.intro_music.stop()
                    if self.game_music.get_num_channels() == 0:
                        self.game_music.play(-1)

        label_mkultra_surface = self.font.render('MK Ultra', False, GameConfig.MENU_TITLE_COLOR)
        label_mkultra_rect = label_mkultra_surface.get_rect(midbottom = (GameConfig.SCREEN_WIDTH / 2, 80))
        label_run_surface = self.font.render('Press <Space> to run', False, GameConfig.MENU_TITLE_COLOR)
        label_run_rect = label_run_surface.get_rect(midbottom = (GameConfig.SCREEN_WIDTH / 2, 350))
        mkultra_label = pygame.transform.scale_by(pygame.image.load('graphics/Player/player_stand.png').convert_alpha(), 2)
        self.screen.blit(label_mkultra_surface, label_mkultra_rect)
        self.screen.blit(label_run_surface, label_run_rect)
        self.screen.blit(mkultra_label, mkultra_label.get_rect(center = (GameConfig.SCREEN_WIDTH / 2, GameConfig.SCREEN_HEIGHT / 2)))


    def show_hiscores(self):
        self.game_music.stop()
        if self.after_game_music.get_num_channels() == 0:
            self.after_game_music.play(-1)
        self.screen.fill(GameConfig.MENU_BACKGROUND_COLOR)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or ( event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                self.keep_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.reset_game()
                    self.mode = 'game'
                    self.after_game_music.stop()
                    if self.game_music.get_num_channels() == 0:
                        self.game_music.play(-1)
            elif event.type == pygame.JOYDEVICEADDED:
                print('Joystick added')
                self.joystick = Joystick(event.device_index)
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 2:
                    self.reset_game()
                    self.mode = 'game'
                    self.after_game_music.stop()
                    if self.game_music.get_num_channels() == 0:
                        self.game_music.play(-1)

        label_mkultra_surface = self.font.render('BUSTED!', False, GameConfig.MENU_TITLE_COLOR)
        label_mkultra_rect = label_mkultra_surface.get_rect(midbottom = (GameConfig.SCREEN_WIDTH / 2, 80))
        label_run_surface = self.font.render('Press <Space> to run', False, GameConfig.MENU_TITLE_COLOR)
        label_run_rect = label_run_surface.get_rect(midbottom = (GameConfig.SCREEN_WIDTH / 2, 350))
        label_score_surface = self.font.render(f'{self.score}', True, (255, 196, 0))
        label_score_surface = pygame.transform.rotozoom(label_score_surface, 45, 1)
        label_score_rect = label_score_surface.get_rect(center = (600, 200))
        mkultra_label = pygame.transform.scale_by(pygame.image.load('graphics/Player/player_stand.png').convert_alpha(), 2)
        self.screen.blit(label_mkultra_surface, label_mkultra_rect)
        self.screen.blit(label_run_surface, label_run_rect)
        self.screen.blit(label_score_surface, label_score_rect)
        self.screen.blit(mkultra_label, mkultra_label.get_rect(center = (GameConfig.SCREEN_WIDTH / 2, GameConfig.SCREEN_HEIGHT / 2)))
    
    def run_mkultra(self):
        print('Launching MK Ultra')

        print(f'Entering game loop in mode {self.mode}')

        while self.keep_running:

            if self.mode == 'splash':
                self.show_splash()
            elif self.mode == 'game':
                self.run_game()
            elif self.mode == 'hiscores':
                self.show_hiscores()

            pygame.display.update()
            self.clock.tick(GameConfig.FPS)

        print('Exited game loop, shutting down MK Ultra.')
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run_mkultra()
