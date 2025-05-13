import pandas as pd
from typing import Optional, List, Dict
from fantraxapi import FantraxAPI
from src.config.config import FANTRAX_LEAGUE_ID, FANTRAX_USER_TEAM_ID, FANTRAX_TEAM_IDS
from src.api.auth import FantraxAuth

class FantraxLeague:
    def __init__(self, league_id: Optional[str] = None):
        self.league_id = league_id or FANTRAX_LEAGUE_ID
        session = FantraxAuth.create_auth_session()
        self.api = FantraxAPI(self.league_id, session=session)

    def get_user_team(self, user_team: Optional[str] = None):
        """Get name of my team in the league"""
        self.user_team = user_team or FANTRAX_USER_TEAM_ID
        return self.api.team(self.user_team)

    def get_my_team_roster_info(self, user_team: Optional[str] = None):
        """Get roster info for User Team"""
        self.user_team = user_team or FANTRAX_USER_TEAM_ID
        return self.api.roster_info(self.user_team)

    def get_all_teams(self, team_ids: Optional[List[str]] = None) -> Dict:
            """Get information for all teams in the league"""
            teams = {}
            team_ids = team_ids or FANTRAX_TEAM_IDS

            for team_id in team_ids:
                try:
                    teams[team_id] = self.api.team(team_id)
                except Exception as e:
                    print(f"Error fetching team {team_id}: {e}")

            return teams

    def get_all_rosters(self, team_ids: Optional[List[str]] = None) -> Dict:
            """Get roster information for all teams in the league"""
            rosters = {}
            team_ids = team_ids or FANTRAX_TEAM_IDS

            for team_id in team_ids:
                try:
                    rosters[team_id] = self.api.roster_info(team_id)
                except Exception as e:
                    print(f"Error fetching roster for team {team_id}: {e}")

            return rosters

    def create_roster_dataframe(self) -> pd.DataFrame:
        """
        Creates a DataFrame containing all players mapped to their respective teams.

        Returns:
            DataFrame with columns: player_name, team_id, team_name
        """
        # Get all teams and rosters
        teams = self.get_all_teams()
        rosters = self.get_all_rosters()

        # Initialize lists to store data
        data = []

        # Iterate through each team and their roster
        for team_id, roster in rosters.items():

            team = teams[team_id]  # Get team object
            team_name = team.name  # Access the name attribute of the Team object

            # Access the players in the roster
            for player in roster.rows:
                # Add to data list
                data.append({
                    'player_name': str(player.player),
                    'team_id': str(team_id),
                    'team_name': str(team_name)
                })

        # Create DataFrame
        df = pd.DataFrame(data).astype({
            'player_name': 'string',
            'team_id': 'string',
            'team_name': 'string'
        })

        return df
