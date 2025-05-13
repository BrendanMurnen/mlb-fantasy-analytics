# src/config/config.py
from datetime import datetime
import os
import json
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

# Project directory setup
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
DB_DIR = DATA_DIR / "duckdb"

# API Configuration
FANTRAX_LEAGUE_ID = os.getenv('FANTRAX_LEAGUE_ID')
FANTRAX_USER_TEAM_ID = os.getenv('FANTRAX_USER_TEAM_ID')
FANTRAX_TEAM_IDS = json.loads(os.getenv('FANTRAX_TEAM_IDS', '[]'))

# Ensure environment variables are loaded
if not all([FANTRAX_LEAGUE_ID, FANTRAX_USER_TEAM_ID, FANTRAX_TEAM_IDS]):
    raise ValueError(
        "Missing required environment variables. "
        "Please ensure FANTRAX_LEAGUE_ID, FANTRAX_USER_TEAM_ID, and FANTRAX_TEAM_IDS "
        "are set in your .env file."
    )

# Ensure directories exist
for dir_path in [RAW_DIR, PROCESSED_DIR, DB_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# Database configuration
DB_PATH = DB_DIR / "baseball.db"

# Data collection configuration
CURRENT_SEASON = datetime.now().year
SEASONS_TO_COLLECT = [CURRENT_SEASON - 2, CURRENT_SEASON - 1, CURRENT_SEASON]  # Current and last two season
