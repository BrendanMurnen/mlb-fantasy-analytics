import duckdb
import pandas as pd
from typing import Optional
from src.config.config import DB_PATH
from src.api.fantrax_client import FantraxLeague

class PlayerAnalyzer:
    def __init__(self, league_id: str):
        self.conn = duckdb.connect(str(DB_PATH))
        self.league = FantraxLeague(league_id)

    def get_player_stats(self, player_names: List[str], stats_type: str = 'batting') -> pd.DataFrame:
        """
        Get stats for specific players
        """
        players_str = "', '".join(player_names)
        query = f"""
            SELECT * FROM {stats_type}_stats
            WHERE Name IN ('{players_str}')
            AND Season >= 2023
        """
        return self.conn.execute(query).fetchdf()

    def analyze_team(self, team_name: Optional[str] = None) -> pd.DataFrame:
        """
        Analyze performance of a specific team's players
        """
        rosters = self.league.get_rostered_players()
        if team_name:
            players = rosters.get(team_name, [])
        else:
            players = self.league.get_my_team_players()

        # Get both batting and pitching stats
        batting_stats = self.get_player_stats(players, 'batting')
        pitching_stats = self.get_player_stats(players, 'pitching')

        # Calculate relevant metrics
        batting_analysis = self._analyze_batting(batting_stats)
        pitching_analysis = self._analyze_pitching(pitching_stats)

        return batting_analysis, pitching_analysis

    def _analyze_batting(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate key batting metrics
        """
        metrics = df.groupby('Name').agg({
            'AVG': 'mean',
            'OBP': 'mean',
            'SLG': 'mean',
            'HR': 'sum',
            'RBI': 'sum',
            'R': 'sum',
            'SB': 'sum',
            'Games': 'sum'
        }).round(3)

        # Add per-game metrics
        metrics['HR/G'] = (metrics['HR'] / metrics['Games']).round(3)
        metrics['RBI/G'] = (metrics['RBI'] / metrics['Games']).round(3)

        return metrics

    def _analyze_pitching(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate key pitching metrics
        """
        metrics = df.groupby('Name').agg({
            'ERA': 'mean',
            'WHIP': 'mean',
            'SO': 'sum',
            'W': 'sum',
            'SV': 'sum',
            'IP': 'sum',
            'G': 'sum'
        }).round(3)

        # Add per-game metrics
        metrics['K/9'] = (metrics['SO'] / metrics['IP'] * 9).round(2)

        return metrics
