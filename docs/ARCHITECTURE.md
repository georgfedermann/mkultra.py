# MK Ultra — Architecture

## Overview

MK Ultra is a Pygame-based "jump and run" game. The player controls a character
that moves left/right and jumps to catch flies and avoid snails. The game runs
at 60 FPS with three screen modes: splash menu, gameplay, and game-over.

## Game Loop

**File:** `src/mkultra/__main__.py` — `Game` class

The game loop runs in `Game.run_mkultra()` as a `while self.keep_running` cycle:

1. **splash** — Title screen. Press Space (or joystick button 2) to start.
2. **game** — Active gameplay. Player moves, enemies spawn, collisions checked.
3. **hiscores** — Game-over screen showing final score. Press Space to restart.

Each iteration processes events, updates sprites, renders to screen, and calls `pygame.display.update()` at 60 FPS.

### Event Timers

- `critter_timer` fires every 1500ms to spawn a new fly or snail (60% fly, 40% snail).
- Music is toggled with `M` key. `Q` quits the game.

## Components

### Player — `Alien` (Sprite)

**File:** `src/mkultra/game/Alien.py`

- Walk: `A` / `D` keys (or joystick axis 0). Animated between two walk frames.
- Jump: `W` / `Space` / joystick button 1. Uses `JUMP_IMPULSE` velocity with gravity.
- Stand: Idle animation when not moving.
- Health: 100 life energy. `apply_damage()` subtracts damage (clamped to 0).
- Lazy-loaded image surfaces via class-level properties.

### Enemies — `Monster` base class

**File:** `src/mkultra/game/Monster.py`

Base `pygame.sprite.Sprite` with:
- Shared `image_cache` class dict for loaded textures.
- 2-frame animation cycle driven by `ANIMATION_SPEED`.
- Position and rect management.

#### Fly

**File:** `src/mkultra/game/Fly.py`

- Spawns at `FLIGHT_LEVEL` (y=216), off-screen right (x=900-1100).
- Moves left at random speed (3-6 px/frame).
- On collision with player: if close enough (delta_y < 6, delta_x < 55), fly is caught (+100 score). Otherwise, fly deals 10 damage and bounces away.
- Catching multiple flies at once triggers achievement sound and restores full health.

#### Snail

**File:** `src/mkultra/game/Snail.py`

- Spawns at `GROUND_LEVEL` (y=300), off-screen right.
- Moves left at 4 px/frame. Deals 20 damage on contact (750ms cooldown).
- On hit: replaced by `SnailExplosion` animation. Explosion continues dealing damage for its duration (1000ms cooldown).
- Once explosion completes, snail sprite is removed from game.

#### SnailExplosion

**File:** `src/mkultra/game/SnailExplosion.py`

- Parses a 12-frame sprite sheet (1152×96, each frame 96×96).
- Animates frames at `ANIMATION_SPEED`. Sets `completed=True` when done.

### UI Widgets

**HealthBar** — `src/mkultra/components/HealthBar.py`

- Renders a green health bar inside a loaded background image.
- Supports percentage 0-1. Uses dirty-flag pattern to avoid unnecessary redraws.
- Includes a glossy gradient effect on the health fill.

**ScoreBoard** — `src/mkultra/game/ScoreBoard.py`

- Renders current score as text in top-right corner.
- Updates every frame to reflect latest score.

### Configuration

**File:** `src/mkultra/game/GameConfig.py`

Class with class-level constants:
| Constant | Value | Description |
|---|---|---|
| FPS | 60 | Target framerate |
| SCREEN_DIMENSION | (800, 400) | Window size |
| GROUND_LEVEL | 300 | Y position of ground |
| FLIGHT_LEVEL | 216 | Y position for flies |
| JUMP_IMPULSE | -20 | Initial jump velocity |
| MOVE_SCALE | 4 | Horizontal movement multiplier |
| FLY_SCORE | 100 | Points per fly caught |
| FLY_DAMAGE | 10 | Damage per fly miss |
| SNAIL_SCORE | 200 | Points per snail hit |
| SNAIL_DAMAGE | 20 | Damage per snail contact |
| ANIMATION_SPEED | 0.1 | Animation frame advance rate |

## Asset Structure

```
graphics/
  Sky.png                  — Background sky
  ground.png               — Ground tile
  Player/                  — Player sprites (stand, walk_1, walk_2, jump)
  Fly/                     — Fly sprites (fly1, fly2)
  snail/                   — Snail sprites (snail1, snail2)
  snail_explosion.png      — 12-frame explosion sprite sheet
  healthbar/background.png — Health bar background
audio/
  music.wav                — Background game music
  intro.mp3                — Splash screen music
  hiscore.mp3              — Game over music
  achievement.mp3          — Multi-fly catch sound
  cjump.mp3                — Jump sound
  punch.mp3                — Fly hit sound
  explosion.wav            — Snail explosion sound
font/
  Pixeltype.ttf            — Pixel font used for UI text
```
