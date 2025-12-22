from pathlib import Path

# src directory (where this file is located)
SRC_DIR = Path(__file__).parent.absolute()

# data directory
DATA_DIR = SRC_DIR / "data"

# Project root (one level up from src)
PROJECT_ROOT = SRC_DIR.parent
