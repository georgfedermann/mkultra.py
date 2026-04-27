# mkultra.py

MK Ultra is a small Pygame jump-and-run game. The player moves an alien left
and right, jumps to catch flies, avoids or stomps snails, and tries to keep
enough health to continue the run.

## Gameplay

- Move left/right with `A` and `D`.
- Jump with `W` or `Space`.
- Catch flies from above to score points.
- Snails damage the player and turn into a short explosion animation when hit.
- Press `M` during gameplay to toggle music.
- Press `Q` to quit.

The game has three modes:

- Splash screen: title screen and start prompt.
- Gameplay: active runner loop with enemy spawning, collisions, score, and health.
- Hiscores: game-over screen showing the final score and restart prompt.

## Project layout

```text
assets/                  Game images, audio, and font files
docs/ARCHITECTURE.md     Runtime and code architecture notes
src/mkultra/__main__.py  Pygame entry point and main game loop
src/mkultra/assets.py    Asset path resolution and cached pygame loaders
src/mkultra/components/  UI sprites such as the health bar
src/mkultra/game/        Player, enemies, score board, and game config
tests/                   Import and configuration smoke tests
```

## Architecture

The main `Game` class owns the Pygame window, event loop, mode transitions,
sprite groups, music, score, and collision handling. Runtime sprites live in
`src/mkultra/game/`, with shared constants in `GameConfig`.

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
