# MK Ultra Architecture

## Overview

MK Ultra is a Pygame-based jump-and-run game. The player controls an alien in a
side-scrolling world, catches flies, avoids or precisely stomps snails, chains
combo attacks, and manages life energy through a cockpit-style HUD.

The project uses a `src/` layout:

```text
src/mkultra/
  __main__.py              Entry point and Game orchestration
  assets.py                Asset path resolution and cached pygame loaders
  components/HealthBar.py  Energy HUD widget
  game/                    Player, enemies, world, effects, scoreboard, config
assets/                    Runtime images, audio, and font files
docs/                      Architecture notes
tests/                     Import and configuration smoke tests
```

## Game Modes

`Game.run_mkultra()` dispatches one frame at a time based on `self.mode`:

| Mode | Purpose |
|---|---|
| `splash` | Title screen. Space or joystick button 2 starts a run. |
| `game` | Active gameplay: input, spawning, world update, collisions, HUD, score. |
| `death` | Zero-energy transition: the player fades, wobbles upward, and disappears. |
| `hiscores` | Game-over screen with final score and restart prompt. |

The `Q` key quits from all modes. During gameplay, `M` toggles background music.

## Runtime Ownership

**File:** `src/mkultra/__main__.py`

The `Game` class is the runtime coordinator. It owns:

- Pygame initialization, display, clock, and event loop.
- Mode transitions.
- Music and generated sound effects.
- Score state and milestone/run-up handling.
- Sprite groups for player, enemies, defeated enemies, combo effects, floating
  score text, and HUD.
- Spawn selection and combo-friendly fly bursts.
- Collision rules for flies, snails, explosions, score, health, and death.

The main loop deliberately keeps HUD and world concerns separate:

- **World-space sprites** use level coordinates and are drawn through `Camera`.
- **HUD sprites** stay in screen coordinates and are drawn directly.

## World, Camera, And Platforms

### Level

**File:** `src/mkultra/game/Level.py`

`Level` owns the side-scrolling world:

- `width`, currently configured by `GameConfig.LEVEL_WIDTH`.
- `camera`, which follows the player horizontally.
- Tiled sky/ground drawing.
- `platforms`, a group of static or moving `Platform` sprites.
- Ground/platform queries used by player movement.

The current level keeps the original runner feel by adding an invisible ground
platform across the full level width. Future level geometry can be added through:

```python
level.add_static_platform(rect)
level.add_moving_platform(rect, velocity, movement_bounds)
```

### Camera

**File:** `src/mkultra/game/Camera.py`

`Camera` stores a horizontal `offset_x`, follows a target rect, and converts
world-space rects into screen-space rects:

```python
screen_rect = camera.apply_rect(world_rect)
```

Enemy spawning is already camera-relative, so monsters appear ahead of the
visible area as the player moves right.

### Platform

**File:** `src/mkultra/game/Platform.py`

`Platform` is a rectangular sprite with optional velocity and movement bounds.
It is intentionally generic so later level work can add:

- static ledges
- moving platforms
- hazards or special surfaces through subclassing or metadata
- boss arenas and locked sections

## Player

**File:** `src/mkultra/game/Alien.py`

`Alien` is the player sprite.

- Movement: `A` / `D`, or joystick axis 0.
- Jump: `W`, `Space`, or joystick button 1.
- Uses level-aware horizontal clamping so the player can eventually move through
  a longer side-scrolling level instead of being constrained to the screen.
- Uses `Level.ground_level_for()` for ground/platform landing.
- Health starts at 100 and `apply_damage()` clamps damage at zero.
- At zero energy, `start_death_animation()` begins the death transition:
  translucent fade, sideways wobble, upward float, then `hiscores`.

## Enemies

### Monster Base

**File:** `src/mkultra/game/Monster.py`

`Monster` provides shared sprite behavior:

- cached image loading by asset path
- two-frame animation cycle
- active/inactive sprite state
- rect setup from a world-space start position

### Fly

**File:** `src/mkultra/game/Fly.py`

Flies spawn at `GameConfig.FLIGHT_LEVEL`, move left with random speed, and can be
stomped from above.

Fly combo behavior is handled in `Game.check_collisions()`:

- single fly stomp: normal fly score
- double fly combo: `DOUBLE_COMBO_SCORE` run-up
- triple fly combo: `TRIPLE_COMBO_SCORE` run-up with stronger effects and siren

When defeated, flies flip over and fall out of the sky.

### Snail

**File:** `src/mkultra/game/Snail.py`

Snails have explicit categories:

- **Volatile snail:** always explodes on contact and damages the player.
- **Stompable snail:** shows a flashing down-arrow. The player must land within
  `SNAIL_WEAK_SPOT_MARGIN` pixels of the arrow center while falling from above.

A successful stomp flips the snail and drops it like a defeated fly. Any failed
touch detonates it into a `SnailExplosion`.

### SnailExplosion

**File:** `src/mkultra/game/SnailExplosion.py`

Uses a 12-frame sprite sheet. Explosion sprites continue animating after the
snail has detonated and can still damage the player while active.

## Spawning

Spawning is handled by `Game.add_critter()` and helper methods:

- `choose_spawn_type()` chooses between fly, fly combo, stompable snail, and
  volatile snail using weights from `GameConfig`.
- `add_fly_combo()` spawns 2-3 flies with controlled spacing so combo stomps are
  intentionally possible.
- `active_monster_count()` prevents overcrowding.
- `random_spawn_x()` uses the camera offset so new enemies appear ahead of the
  current view in level coordinates.

This is ready for a future difficulty director. The next step would be to vary
weights, spawn timing, and max active monsters by elapsed time, score, or level
section.

## Score And Combo Effects

### ScoreBoard

**File:** `src/mkultra/game/ScoreBoard.py`

The scoreboard is a compact cockpit HUD panel. It displays a zero-padded score,
segment meter, glow flashes, and milestone highlights.

Score changes flow through:

- `Game.add_score(points)` for immediate score changes.
- `Game.add_score_runup(points, with_siren=False)` for animated score increases.

The run-up increments by `SCORE_RUNUP_STEP` every
`SCORE_RUNUP_INTERVAL_MS`, playing repeated tick sounds.

### ComboEffect

**File:** `src/mkultra/game/ComboEffect.py`

Renders flashy star effects around the player after multi-fly stomp attacks.
Triple combos use stronger rings and more stars.

### FloatingScore

**File:** `src/mkultra/game/FloatingScore.py`

Shows `+1000 COMBO` or `+2000 COMBO` near the player while the scoreboard runs
up.

## HUD

### HealthBar

**File:** `src/mkultra/components/HealthBar.py`

The health bar is rendered as a spaceship-style energy panel:

- smaller cockpit frame
- color interpolation from green to orange to red
- blinking below 10%
- warning lamp and siren for critical energy

The color fade uses RGB linear interpolation in `_lerp_color()`.

## Assets

**File:** `src/mkultra/assets.py`

Asset loading is centralized:

| Helper | Purpose |
|---|---|
| `asset_path(*parts)` | Builds absolute paths inside `assets/`. |
| `load_image(relative_path)` | Loads and caches converted image surfaces. |
| `load_sound(relative_path)` | Loads and caches `pygame.mixer.Sound`. |
| `load_font(relative_path, size)` | Loads and caches fonts by path and size. |

Game code should pass paths relative to `assets/`, for example:

```python
load_image('graphics/Player/player_stand.png')
```

## Configuration

**File:** `src/mkultra/game/GameConfig.py`

`GameConfig` contains class-level tuning constants. Important groups:

- screen and FPS
- player movement, death animation, and level width
- camera target ratio
- fly score, damage, combo spawn spacing, and combo rewards
- snail damage, spawn weights, and weak-spot margin
- score run-up timing
- active monster cap and spawn distance

## Extension Points

The current architecture is prepared for:

- longer right-scrolling levels
- static and moving platform layouts
- power-ups and pickups as new world-space sprites
- environmental hazards
- mission objectives and combo meters
- end-of-level boss arenas

Recommended next structural step: move spawn/difficulty rules out of `Game` into
a dedicated director class once difficulty phases, power-ups, and boss triggers
become concrete.
