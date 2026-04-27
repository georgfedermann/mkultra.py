"""Verify all modules import correctly."""
from mkultra.assets import asset_path
from mkultra.components.HealthBar import HealthBar
from mkultra.game.Alien import Alien
from mkultra.game.Fly import Fly
from mkultra.game.GameConfig import GameConfig
from mkultra.game.Monster import Monster
from mkultra.game.ScoreBoard import ScoreBoard
from mkultra.game.Snail import Snail
from mkultra.game.SnailExplosion import SnailExplosion


def test_modules_import():
    assert Alien
    assert Fly
    assert HealthBar
    assert Monster
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
