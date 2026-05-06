import random
from array import array
from math import pi, sin

import pygame
from pygame.joystick import Joystick
from pygame.sprite import Group, GroupSingle

from mkultra.assets import load_font, load_image, load_sound
from mkultra.components.HealthBar import HealthBar
from mkultra.game.Alien import Alien
from mkultra.game.ComboEffect import ComboEffect
from mkultra.game.FloatingScore import FloatingScore
from mkultra.game.Fly import Fly
from mkultra.game.GameConfig import GameConfig
from mkultra.game.Level import Level
from mkultra.game.PlatformerAtlas import platformer_atlas
from mkultra.game.ScoreBoard import ScoreBoard
from mkultra.game.Snail import Snail


class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(GameConfig.SCREEN_DIMENSION)
        pygame.display.set_caption('MK Ultra')

        self.level = Level()
        self.font = load_font('font/Pixeltype.ttf', 50)

        self.score = 0
        self.score_board = ScoreBoard(self)
        self.score_board.set_score(self.score)

        self.alien = GroupSingle()
        self.alien.add(Alien())
        self.health_bar = HealthBar((10, 10), self.alien.sprite.life_energy / self.alien.sprite.max_life_energy)

        self.fly_group = Group()
        self.snail_group = Group()
        self.combo_effect_group = Group()
        self.floating_score_group = Group()
        self.defeated_critter_group = Group()
        self.hud_group = Group()
        self.hud_group.add(self.health_bar)
        self.hud_group.add(self.score_board)

        self.clock = pygame.time.Clock()
        self.critter_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.critter_timer, 1500)

        self.keep_running = True
        self.mode = 'splash'

        self.game_music = load_sound('audio/music.wav')
        self.game_music.set_volume(0.2)

        self.intro_music = load_sound('audio/intro.mp3')
        self.intro_music.set_volume(0.2)

        self.after_game_music = load_sound('audio/hiscore.mp3')
        self.after_game_music.set_volume(0.2)
        self.achievement_sound = load_sound('audio/achievement.mp3')
        self.warning_siren = self.create_warning_siren()
        self.warning_siren.set_volume(0.35)
        self.score_chime = self.create_score_chime()
        self.score_chime.set_volume(0.45)
        self.score_fanfare = self.create_score_fanfare()
        self.score_fanfare.set_volume(0.55)
        self.score_tick = self.create_score_tick()
        self.score_tick.set_volume(0.35)
        self.combo_siren = self.create_warning_siren()
        self.combo_siren.set_volume(0.28)
        self.score_runup_remaining = 0
        self.next_score_runup_at = 0

    def reset_game(self):
        self.alien.add(Alien())
        self.level = Level()
        self.fly_group.empty()
        self.snail_group.empty()
        self.combo_effect_group.empty()
        self.floating_score_group.empty()
        self.defeated_critter_group.empty()
        self.set_player_health_bar()
        self.score = 0
        self.score_board.set_score(self.score)
        self.warning_siren.stop()
        self.combo_siren.stop()
        self.score_runup_remaining = 0

    def create_warning_siren(self) -> pygame.mixer.Sound:
        sample_rate = 44100
        sound_format = -16
        channels = 2

        mixer_config = pygame.mixer.get_init()
        if mixer_config:
            sample_rate, sound_format, channels = mixer_config

        sample_count = sample_rate
        max_amplitude = 32767 if sound_format < 0 else 255
        samples = array("h")
        for index in range(sample_count):
            progress = index / sample_count
            frequency = 620 + 280 * sin(2 * pi * progress)
            tone = int(max_amplitude * 0.45 * sin(2 * pi * frequency * index / sample_rate))
            pulse = 1 if int(progress * 8) % 2 == 0 else 0.42
            value = int(tone * pulse)
            for _ in range(channels):
                samples.append(value)

        return pygame.mixer.Sound(buffer=samples)

    def create_score_chime(self) -> pygame.mixer.Sound:
        return self.create_tone_sequence([(659, 0.08), (880, 0.1), (1318, 0.18)], volume=0.42)

    def create_score_fanfare(self) -> pygame.mixer.Sound:
        return self.create_tone_sequence([(523, 0.08), (659, 0.08), (784, 0.08), (1046, 0.2), (1568, 0.18)], volume=0.48)

    def create_score_tick(self) -> pygame.mixer.Sound:
        return self.create_tone_sequence([(1174, 0.025)], volume=0.34)

    def create_tone_sequence(self, notes, volume=0.4) -> pygame.mixer.Sound:
        sample_rate = 44100
        sound_format = -16
        channels = 2

        mixer_config = pygame.mixer.get_init()
        if mixer_config:
            sample_rate, sound_format, channels = mixer_config

        max_amplitude = 32767 if sound_format < 0 else 255
        samples = array("h")
        for frequency, duration in notes:
            sample_count = int(sample_rate * duration)
            for index in range(sample_count):
                envelope = 1 - (index / sample_count)
                value = int(max_amplitude * volume * envelope * sin(2 * pi * frequency * index / sample_rate))
                for _ in range(channels):
                    samples.append(value)

        return pygame.mixer.Sound(buffer=samples)

    def set_player_health_bar(self):
        health_percentage = max(0, self.alien.sprite.life_energy / self.alien.sprite.max_life_energy)
        self.health_bar.set_percentage(health_percentage)
        self.update_warning_siren(health_percentage)

    def update_warning_siren(self, health_percentage):
        if self.mode == 'game' and 0 < health_percentage <= HealthBar.CRITICAL_THRESHOLD:
            if self.warning_siren.get_num_channels() == 0:
                self.warning_siren.play(-1)
        else:
            self.warning_siren.stop()

    def add_score(self, points):
        previous_score = self.score
        self.score += points
        self.score_board.set_score(self.score)
        self.play_score_milestone(previous_score, self.score)

    def add_score_runup(self, points, with_siren=False):
        self.score_runup_remaining += points
        self.next_score_runup_at = pygame.time.get_ticks()
        self.score_board.flash(level=2)
        if with_siren and self.combo_siren.get_num_channels() == 0:
            self.combo_siren.play(-1)

    def update_score_runup(self):
        if self.score_runup_remaining <= 0:
            self.combo_siren.stop()
            return

        current_time = pygame.time.get_ticks()
        if current_time < self.next_score_runup_at:
            return

        step = min(GameConfig.SCORE_RUNUP_STEP, self.score_runup_remaining)
        self.score_runup_remaining -= step
        self.next_score_runup_at = current_time + GameConfig.SCORE_RUNUP_INTERVAL_MS
        self.add_score(step)
        self.score_tick.play()

        if self.score_runup_remaining <= 0:
            self.combo_siren.stop()

    def play_score_milestone(self, previous_score, current_score):
        previous_major = previous_score // 10000
        current_major = current_score // 10000
        if current_major > previous_major:
            self.score_fanfare.play()
            self.score_board.flash(level=2)
            return

        previous_minor = previous_score // 1000
        current_minor = current_score // 1000
        if current_minor > previous_minor:
            self.score_chime.play()
            self.score_board.flash(level=1)

    def add_critter(self):
        if self.active_monster_count() >= GameConfig.MAX_ACTIVE_MONSTERS:
            return

        spawn_type = self.choose_spawn_type()
        if spawn_type == 'fly_combo':
            self.add_fly_combo()
        elif spawn_type == 'stompable_snail':
            self.snail_group.add(Snail(can_be_stomped=True, start_x=self.random_spawn_x()))
        elif spawn_type == 'volatile_snail':
            self.snail_group.add(Snail(can_be_stomped=False, start_x=self.random_spawn_x()))
        else:
            self.fly_group.add(Fly(start_x=self.random_spawn_x()))

    def active_monster_count(self):
        return len(self.fly_group) + len(self.snail_group)

    def choose_spawn_type(self):
        spawn_weights = [
            ('fly', GameConfig.FLY_SPAWN_WEIGHT),
            ('stompable_snail', GameConfig.STOMPABLE_SNAIL_SPAWN_WEIGHT),
            ('volatile_snail', GameConfig.VOLATILE_SNAIL_SPAWN_WEIGHT),
        ]
        total_weight = sum(weight for _, weight in spawn_weights)
        roll = random.randint(1, total_weight)
        for spawn_type, weight in spawn_weights:
            if roll <= weight:
                if spawn_type == 'fly' and random.randint(1, 100) <= GameConfig.FLY_COMBO_CHANCE:
                    return 'fly_combo'
                return spawn_type
            roll -= weight

        return 'fly'

    def add_fly_combo(self):
        available_slots = GameConfig.MAX_ACTIVE_MONSTERS - self.active_monster_count()
        combo_size = min(random.randint(GameConfig.FLY_COMBO_MIN_SIZE, GameConfig.FLY_COMBO_MAX_SIZE), available_slots)
        start_x = self.random_spawn_x()
        spacing = random.randint(GameConfig.FLY_COMBO_MIN_SPACING, GameConfig.FLY_COMBO_MAX_SPACING)

        for index in range(combo_size):
            self.fly_group.add(Fly(start_x=start_x + index * spacing))

    def random_spawn_x(self):
        spawn_min = self.level.camera.offset_x + GameConfig.SPAWN_X_MIN
        spawn_max = self.level.camera.offset_x + GameConfig.SPAWN_X_MAX
        return min(random.randint(spawn_min, spawn_max), self.level.width - 40)

    def is_stomp_from_above(self, player, critter):
        delta_x = abs(player.rect.centerx - critter.rect.centerx)
        vertical_overlap = player.rect.bottom - critter.rect.top
        max_stomp_depth = max(12, player.dy + 4)
        return player.dy >= 0 and 0 <= vertical_overlap <= max_stomp_depth and delta_x < 55

    def check_collisions(self):
        # flies
        collision_flies = pygame.sprite.spritecollide(self.alien.sprite, self.fly_group, True)
        player = self.alien.sprite
        if collision_flies:
            hit_count = 0

            for fly in collision_flies:
                if self.is_stomp_from_above(player, fly):
                    self.defeated_critter_group.add(fly)
                    fly.hit()
                    hit_count += 1
                else:
                    self.fly_group.add(fly)
                    if fly.can_do_damage(pygame.time.get_ticks()):
                        fly.set_damage_time(pygame.time.get_ticks())
                        player.apply_damage(GameConfig.FLY_DAMAGE)
                        self.set_player_health_bar()
                        if player.life_energy <= 0:
                            self.end_game()
                            return

            if hit_count >= 3:
                self.start_combo_attack(hit_count, GameConfig.TRIPLE_COMBO_SCORE)
                player.life_energy = player.max_life_energy
                self.set_player_health_bar()
            elif hit_count == 2:
                self.start_combo_attack(hit_count, GameConfig.DOUBLE_COMBO_SCORE)
                player.life_energy = player.max_life_energy
                self.set_player_health_bar()
            elif hit_count == 1:
                self.add_score(GameConfig.FLY_SCORE)

        # snails
        snails = pygame.sprite.spritecollide(self.alien.sprite, self.snail_group, False)
        if snails:
            for snail in snails:
                if not snail.explosion and snail.is_hit_in_weak_spot(player):
                    self.snail_group.remove(snail)
                    self.defeated_critter_group.add(snail)
                    self.add_score(GameConfig.SNAIL_SCORE)
                    snail.stomp()
                    continue

                # Direct snail contact always detonates unless the marked weak spot was hit.
                if not snail.explosion:
                    player.apply_damage(GameConfig.SNAIL_DAMAGE)
                    self.set_player_health_bar()
                    snail.set_damage_time(pygame.time.get_ticks())
                    snail.hit()
                    if player.life_energy <= 0:
                        self.end_game()
                        return
                # Check if explosion exists and can do damage
                elif snail.explosion and not snail.is_explosion_complete():
                    # Only do damage if explosion is not in cooldown
                    if snail.can_explosion_do_damage(pygame.time.get_ticks()):
                        player.apply_damage(GameConfig.SNAIL_DAMAGE)
                        self.set_player_health_bar()
                        snail.set_explosion_damage_time(pygame.time.get_ticks())
                        if player.life_energy <= 0:
                            self.end_game()
                            return

        # Remove snails whose explosions have completed
        for snail in self.snail_group.sprites():
            if snail.explosion and snail.is_explosion_complete():
                snail.kill()

    def start_combo_attack(self, hit_count, score):
        self.combo_effect_group.add(ComboEffect(self.alien.sprite.rect.center, hit_count))
        self.floating_score_group.add(FloatingScore(self.alien.sprite.rect.center, score, hit_count))
        self.achievement_sound.play()
        self.add_score_runup(score, with_siren=hit_count >= 3)

    def end_game(self):
        if self.mode == 'death':
            return

        self.mode = 'death'
        self.warning_siren.stop()
        self.combo_siren.stop()
        self.alien.sprite.start_death_animation()

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

        self.update_score_runup()

        self.alien.update(self.level)
        self.level.update(self.alien.sprite.rect)
        self.fly_group.update()
        self.snail_group.update()
        self.combo_effect_group.update()
        self.floating_score_group.update()
        self.defeated_critter_group.update()
        self.hud_group.update()
        self.draw_world()

        self.check_collisions()

    def run_death_animation(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                self.keep_running = False

        self.update_score_runup()

        self.alien.update()
        self.level.update(self.alien.sprite.rect)
        self.fly_group.update()
        self.snail_group.update()
        self.combo_effect_group.update()
        self.floating_score_group.update()
        self.defeated_critter_group.update()
        self.hud_group.update()
        self.draw_world()

        if self.alien.sprite.is_death_animation_complete():
            self.mode = 'hiscores'

    def draw_world(self):
        self.level.draw_background(self.screen)
        self.level.draw_platforms(self.screen)
        self.draw_sprite_group(self.fly_group)
        self.draw_snails()
        self.draw_sprite_group(self.defeated_critter_group)
        self.draw_sprite_group(self.combo_effect_group)
        self.draw_sprite_group(self.floating_score_group)
        self.screen.blit(self.alien.sprite.image, self.level.camera.apply_rect(self.alien.sprite.rect))
        self.hud_group.draw(self.screen)

    def draw_sprite_group(self, group):
        visible_area = self.level.camera.visible_area()
        for sprite in group.sprites():
            if sprite.rect.colliderect(visible_area):
                self.screen.blit(sprite.image, self.level.camera.apply_rect(sprite.rect))

    def draw_snails(self):
        visible_area = self.level.camera.visible_area()
        for snail in self.snail_group.sprites():
            if not snail.rect.colliderect(visible_area):
                continue

            if snail.should_draw_snail():
                self.screen.blit(snail.image, self.level.camera.apply_rect(snail.rect))
                snail.draw_marker(self.screen, self.level.camera)
            elif snail.explosion:
                snail.explosion.update()
                self.screen.blit(snail.explosion.image, self.level.camera.apply_rect(snail.explosion.rect))

    def show_splash(self):
        self.game_music.stop()
        self.warning_siren.stop()
        self.combo_siren.stop()
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
                if event.button == 2:
                    self.reset_game()
                    self.mode = 'game'
                    self.intro_music.stop()
                    if self.game_music.get_num_channels() == 0:
                        self.game_music.play(-1)

        label_mkultra_surface = self.font.render('MK Ultra', False, GameConfig.MENU_TITLE_COLOR)
        label_mkultra_rect = label_mkultra_surface.get_rect(midbottom = (GameConfig.SCREEN_WIDTH / 2, 80))
        label_run_surface = self.font.render('Press <Space> to run', False, GameConfig.MENU_TITLE_COLOR)
        label_run_rect = label_run_surface.get_rect(midbottom = (GameConfig.SCREEN_WIDTH / 2, 350))
        mkultra_label = pygame.transform.scale_by(load_image('graphics/Player/player_stand.png'), 2)
        self.screen.blit(label_mkultra_surface, label_mkultra_rect)
        self.screen.blit(label_run_surface, label_run_rect)
        self.screen.blit(mkultra_label, mkultra_label.get_rect(center = (GameConfig.SCREEN_WIDTH / 2, GameConfig.SCREEN_HEIGHT / 2)))

    def show_hiscores(self):
        self.game_music.stop()
        self.warning_siren.stop()
        self.combo_siren.stop()
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
        mkultra_label = pygame.transform.scale_by(platformer_atlas().sprite('player_dance'), 2)
        self.screen.blit(label_mkultra_surface, label_mkultra_rect)
        self.screen.blit(label_run_surface, label_run_rect)
        self.screen.blit(label_score_surface, label_score_rect)
        self.screen.blit(mkultra_label, mkultra_label.get_rect(center = (GameConfig.SCREEN_WIDTH / 2, GameConfig.SCREEN_HEIGHT / 2)))

    def run_mkultra(self):
        while self.keep_running:
            if self.mode == 'splash':
                self.show_splash()
            elif self.mode == 'game':
                self.run_game()
            elif self.mode == 'death':
                self.run_death_animation()
            elif self.mode == 'hiscores':
                self.show_hiscores()

            pygame.display.update()
            self.clock.tick(GameConfig.FPS)

        pygame.quit()


def main():
    game = Game()
    game.run_mkultra()


if __name__ == '__main__':
    main()
