from datetime import datetime
import pandas as pd
from pybaseball import batting_stats_bref, pitching_stats_bref
from src.config.config import RAW_DIR, SEASONS_TO_COLLECT
from src.api.fantrax_client import FantraxLeague

class MLBDataExtractor:
    def __init__(self):
        self.current_season = datetime.now().year
        self.league = FantraxLeague()

    def fetch_batting_stats(self, season: int) -> pd.DataFrame:
        """Fetch batting statistics for a given season."""
        print(f"Fetching batting stats for {season}")
        return batting_stats_bref(season)

    def fetch_pitching_stats(self, season: int) -> pd.DataFrame:
        """Fetch pitching statistics for a given season."""
        print(f"Fetching pitching stats for {season}")
        return pitching_stats_bref(season)

    def save_raw_season_data(self, df: pd.DataFrame, name: str, season: int):
        """Save raw data to parquet file."""
        filename = RAW_DIR / f"{name}_{season}.parquet"
        df.to_parquet(filename)
        print(f"Saved {filename}")

    def extract_roster_assignments(self):
            """Extract current roster assignments from Fantrax."""
            print("Fetching current roster assignments")
            try:
                # Get roster DataFrame using the existing method
                roster_df = self.league.create_roster_dataframe()

                # Add timestamp
                roster_df['extract_date'] = datetime.now().date()

                # Save to parquet file
                filename = RAW_DIR / f"roster_assignments_{datetime.now().strftime('%Y%m%d')}.parquet"
                roster_df.to_parquet(filename)
                print(f"Saved roster assignments to {filename}")

                return roster_df

            except Exception as e:
                print(f"Error extracting roster assignments: {e}")
                return None

    def extract_all_stats(self):
        """Extract all stats for configured seasons."""
        # Extract roster assignments first
        print("Extracting roster assignments...")
        self.extract_roster_assignments()

        # Continue with existing stats extraction
        for season in SEASONS_TO_COLLECT:
            # Fetch and save batting stats
            batting_df = self.fetch_batting_stats(season)
            self.save_raw_season_data(batting_df, "batting", season)

            # Fetch and save pitching stats
            pitching_df = self.fetch_pitching_stats(season)
            self.save_raw_season_data(pitching_df, "pitching", season)
