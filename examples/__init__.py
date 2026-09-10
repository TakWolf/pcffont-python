from pathlib import Path

PROJECT_ROOT_DIR = Path(__file__).parent.joinpath('..').resolve()
ASSETS_DIR = PROJECT_ROOT_DIR.joinpath('assets')
BUILD_DIR = PROJECT_ROOT_DIR.joinpath('build')
