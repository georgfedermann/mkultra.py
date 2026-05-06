"""Verify all modules import correctly."""
from mkultra.assets import asset_path
from mkultra.components.HealthBar import HealthBar
from mkultra.game.Alien import Alien
from mkultra.game.ComboEffect import ComboEffect
from mkultra.game.FloatingScore import FloatingScore
from mkultra.game.Fly import Fly
from mkultra.game.GameConfig import GameConfig
from mkultra.game.Level import Level
from mkultra.game.Monster import Monster
from mkultra.game.Platform import Platform
from mkultra.game.PlatformerAtlas import PlatformerAtlas
from mkultra.game.ScoreBoard import ScoreBoard
from mkultra.game.Snail import Snail
from mkultra.game.SnailExplosion import SnailExplosion


def test_modules_import():
    assert Alien
    assert ComboEffect
    assert Fly
    assert FloatingScore
    assert HealthBar
    assert Level
    assert Monster
    assert Platform
    assert PlatformerAtlas
    assert ScoreBoard
    assert Snail
    assert SnailExplosion


def test_game_config_defaults():
    assert GameConfig.FPS == 60
    assert GameConfig.SCREEN_DIMENSION == (800, 400)
    assert GameConfig.GROUND_LEVEL == 300
    assert GameConfig.FLY_SCORE == 100
    assert GameConfig.SNAIL_SCORE == 200


def test_asset_path_resolves_project_assets():
    assert asset_path('font/Pixeltype.ttf').is_file()


def test_platformer_atlas_uses_reported_sprite_locations():
    assert PlatformerAtlas.RECTS['player_stand'].x == 440
    assert PlatformerAtlas.RECTS['player_walk_1'].x == 646
    assert PlatformerAtlas.RECTS['player_jump'].x == 484
    assert PlatformerAtlas.RECTS['player_walk_2'].x == 668
    assert PlatformerAtlas.RECTS['player_climb_1'].x == 554
    assert PlatformerAtlas.RECTS['player_climb_2'].x == 577
    assert PlatformerAtlas.RECTS['player_death'].x == 531
    assert PlatformerAtlas.RECTS['fly_1'] == (300, 328, 22, 20)
    assert PlatformerAtlas.RECTS['fly_2'] == (324, 327, 22, 20)
    assert PlatformerAtlas.RECTS['coin'] == (416, 50, 22, 20)
    assert PlatformerAtlas.RECTS['heart_full'] == (436, 95, 22, 20)
    assert PlatformerAtlas.RECTS['heart_empty'] == (484, 95, 22, 20)


def test_alien_uses_platformer_atlas_player_frames():
    Alien._alien_stand_surface = None
    Alien._alien_walk1_surface = None
    Alien._alien_walk2_surface = None
    Alien._alien_jump_surface = None

    assert Alien.__new__(Alien).alien_stand_surface.get_size() == (88, 84)
    assert Alien.__new__(Alien).alien_walk1_surface.get_size() == (88, 84)
    assert Alien.__new__(Alien).alien_walk2_surface.get_size() == (88, 84)
    assert Alien.__new__(Alien).alien_jump_surface.get_size() == (88, 84)
    assert Alien.__new__(Alien).alien_stand_surface.get_at((0, 0)).a == 0


def test_platformer_atlas_uses_real_transparency():
    atlas = PlatformerAtlas()

    assert atlas.sprite('player_stand').get_at((0, 0)).a == 0
    assert atlas.sprite('fly_1').get_at((0, 0)).a == 0


def test_fly_uses_platformer_atlas_frames():
    fly = Fly()

    assert fly.image.get_size() == (88, 80)
    assert fly.image.get_at((0, 0)).a == 0


def test_alien_damage_clamps_at_zero():
    alien = Alien.__new__(Alien)
    alien.max_life_energy = 100
    alien.life_energy = alien.max_life_energy

    alien.apply_damage(alien.max_life_energy)
    alien.apply_damage(10)

    assert alien.life_energy == 0
