# mkultra.py

MK Ultra is a small Pygame jump-and-run game. The player moves an alien through
a side-scrolling level, jumps to catch flies, reads snail danger signals, chains
combo stomps, and tries to keep enough energy to continue the run.

## Gameplay

- Move left/right with `A` and `D`.
- Jump with `W` or `Space`.
- Catch flies from above to score points.
- Chain fly stomps for combo attacks. Double combos award 1000 points, triple
  combos award 2000 points with stronger star effects, siren, floating score
  text, and a ticking score run-up.
- Avoid volatile snails. They explode on touch.
- Stomp only the snails marked by the flashing down-arrow, and land close to the
  arrow center or the snail still explodes.
- Watch the cockpit-style energy bar. It shifts from green to orange to red,
  blinks below 10%, and plays a warning siren until energy recovers.
- Press `M` during gameplay to toggle music.
- Press `Q` to quit.

The game has four modes:

- Splash screen: title screen and start prompt.
- Gameplay: active runner loop with enemy spawning, collisions, score, and health.
- Death animation: the player becomes translucent, wobbles upward, and vanishes
  before the game-over screen.
- Hiscores: game-over screen showing the final score and restart prompt.

## Project layout

```text
assets/                  Game images, audio, and font files
docs/ARCHITECTURE.md     Runtime and code architecture notes
src/mkultra/__main__.py  Pygame entry point and main game loop
src/mkultra/assets.py    Asset path resolution and cached pygame loaders
src/mkultra/components/  HUD components such as the health bar
src/mkultra/game/        Player, enemies, level, camera, effects, config
tests/                   Import and configuration smoke tests
```

## Architecture

The main `Game` class owns the Pygame window, event loop, mode transitions,
sprite groups, music, score, and collision handling. The active world is managed
by `Level`, which owns the side-scrolling camera, tiled ground, and platform
collection. Runtime sprites and effects live in `src/mkultra/game/`, with shared
constants in `GameConfig`.

The code is prepared for larger level extensions: the player already moves in
level coordinates, actors render through a camera, and `Platform` supports
static and moving platform geometry.

Asset loading is centralized in `src/mkultra/assets.py`. Game code should load
images, sounds, and fonts through `load_image()`, `load_sound()`, and
`load_font()` using paths relative to the top-level `assets/` directory.
Those helpers cache pygame resources so callers do not need to duplicate
repository-relative path logic or local caches.

## Installation

This project uses Poetry for dependency management.

### Prerequisites

- Python 3.10 or higher
- Poetry (https://python-poetry.org/)

### Setup

```bash
poetry install
```

## Run

```bash
poetry run mkultra
```

## Development

```bash
poetry run pytest
poetry run ruff check src tests
```

For a deeper explanation of the game loop, sprites, assets, and module
responsibilities, see `docs/ARCHITECTURE.md`.
