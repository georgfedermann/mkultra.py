# MK Ultra — Architecture

## Overview

MK Ultra is a Pygame-based "jump and run" game. The player controls a character
that moves left/right and jumps to catch flies and avoid snails. The game runs
at 60 FPS with three screen modes: splash menu, gameplay, and game-over.

The project uses a `src/` layout:

```text
src/mkultra/
  __main__.py             Entry point and main Game orchestration
  assets.py               Asset path resolution and cached pygame loaders
  components/HealthBar.py Health bar UI sprite
  game/                   Player, enemies, scoreboard, and configuration
assets/                   Runtime images, audio, and font files
tests/                    Import and configuration smoke tests
```

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

### Runtime Ownership

The `Game` class owns:

- Pygame initialization, display setup, clock, and quit handling.
- Mode state (`splash`, `game`, `hiscores`) and mode transitions.
- Sprite groups for the player, flies, snails, dead critters, health bar, and score board.
- Background surfaces, UI font, music, and achievement sound handles.
- Collision rules that update score, health, enemy state, and game-over state.

## Components

### Player — `Alien` (Sprite)

**File:** `src/mkultra/game/Alien.py`

- Walk: `A` / `D` keys (or joystick axis 0). Animated between two walk frames.
- Jump: `W` / `Space` / joystick button 1. Uses `JUMP_IMPULSE` velocity with gravity.
- Stand: Idle animation when not moving.
- Health: 100 life energy. `apply_damage()` subtracts damage (clamped to 0).
- Animation images are exposed through class-level properties backed by the shared asset loader.
- Jump sound is loaded through the shared asset loader and reused by the player instance.

### Enemies — `Monster` base class

**File:** `src/mkultra/game/Monster.py`

Base `pygame.sprite.Sprite` with:
- Shared `image_cache` class dict keyed by relative asset path.
- 2-frame animation cycle driven by `ANIMATION_SPEED`.
- Position and rect management.
- Image loading delegated to `mkultra.assets.load_image()`.

#### Fly

**File:** `src/mkultra/game/Fly.py`

- Spawns at `FLIGHT_LEVEL` (y=216), off-screen right (x=900-1100).
- Moves left at random speed (3-6 px/frame).
- On collision with player: if close enough (delta_y < 6, delta_x < 55), fly is caught (+100 score). Otherwise, fly deals 10 damage and bounces away.
- Catching multiple flies at once triggers achievement sound and restores full health.
- Uses `graphics/Fly/Fly1.png` and `graphics/Fly/Fly2.png` for animation.

#### Snail

**File:** `src/mkultra/game/Snail.py`

- Spawns at `GROUND_LEVEL` (y=300), off-screen right.
- Moves left at 4 px/frame. Deals 20 damage on contact (750ms cooldown).
- On hit: replaced by `SnailExplosion` animation. Explosion continues dealing damage for its duration (1000ms cooldown).
- Once explosion completes, snail sprite is removed from game.
- Uses `graphics/snail/snail1.png` and `graphics/snail/snail2.png` for animation.

#### SnailExplosion

**File:** `src/mkultra/game/SnailExplosion.py`

- Parses a 12-frame sprite sheet (1152×96, each frame 96×96).
- Animates frames at `ANIMATION_SPEED`. Sets `completed=True` when done.
- Sprite sheet is loaded once via `mkultra.assets.load_image()`.

### UI Widgets

**HealthBar** — `src/mkultra/components/HealthBar.py`

- Renders a green health bar inside a loaded background image.
- Supports percentage 0-1. Uses dirty-flag pattern to avoid unnecessary redraws.
- Includes a glossy gradient effect on the health fill.

**ScoreBoard** — `src/mkultra/game/ScoreBoard.py`

- Renders current score as text in top-right corner.
- Updates every frame to reflect latest score.

## Asset Loading

**File:** `src/mkultra/assets.py`

Asset loading is centralized behind four helpers:

| Helper | Purpose |
|---|---|
| `ASSET_ROOT` | Absolute path to the top-level `assets/` directory |
| `asset_path(*parts)` | Builds absolute paths inside `assets/` |
| `load_image(relative_path)` | Loads and caches `pygame.Surface` objects with `convert_alpha()` |
| `load_sound(relative_path)` | Loads and caches `pygame.mixer.Sound` objects |
| `load_font(relative_path, size)` | Loads and caches `pygame.font.Font` objects by path and size |

Callers pass paths relative to `assets/`, for example
`load_image('graphics/Player/player_stand.png')`. This keeps repository layout
knowledge in one module and avoids repeated `Path(__file__)` calculations across
sprites and UI components.

Pygame image, sound, and font loading still requires the relevant Pygame systems
to be initialized before game objects are constructed. `Game.__init__()` calls
`pygame.init()` before loading runtime resources.

## Configuration

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
assets/
  graphics/
    Sky.png                  — Background sky
    ground.png               — Ground tile
    Player/                  — Player sprites (stand, walk_1, walk_2, jump)
    Fly/                     — Fly sprites (Fly1, Fly2)
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
