"""Verify all modules import correctly."""
from mkultra.game.Alien import Alien
from mkultra.game.Fly import Fly
from mkultra.game.GameConfig import GameConfig
from mkultra.game.Monster import Monster
from mkultra.game.ScoreBoard import ScoreBoard
from mkultra.game.Snail import Snail
from mkultra.game.SnailExplosion import SnailExplosion
from mkultra.components.HealthBar import HealthBar


def test_game_config_defaults():
    assert GameConfig.FPS == 60
    assert GameConfig.SCREEN_DIMENSION == (800, 400)
    assert GameConfig.GROUND_LEVEL == 300
    assert GameConfig.FLY_SCORE == 100
    assert GameConfig.SNAIL_SCORE == 200
