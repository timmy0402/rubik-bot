from pathlib import Path

"""
Centralized path definitions for the project.
Uses pathlib for cross-platform compatibility.
"""

# Absolute path to the src directory (where this file is located)
SRC_DIR = Path(__file__).parent.absolute()

# Path to the data directory containing static assets like algorithms.json
DATA_DIR = SRC_DIR / "data"

# Project root directory (one level up from src)
PROJECT_ROOT = SRC_DIR.parent