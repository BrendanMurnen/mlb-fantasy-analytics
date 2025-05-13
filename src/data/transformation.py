# src/data/transformation.py
import duckdb
from src.config.config import RAW_DIR, DB_PATH

class MLBDataTransformer:
    def __init__(self):
        self.conn = duckdb.connect(str(DB_PATH))

    def setup_database(self):
        """Create necessary tables in DuckDB."""
        # Updated batting_stats schema based on Baseball Reference data
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS source_bref__batting_stats (
                mlbID VARCHAR,
                Name VARCHAR,
                Age INTEGER,
                Team VARCHAR,
                Season INTEGER,
                Games INTEGER,
                PA INTEGER,
                AB INTEGER,
                R INTEGER,
                H INTEGER,
                doubles INTEGER,
                triples INTEGER,
                HR INTEGER,
                RBI INTEGER,
                BB INTEGER,
                IBB INTEGER,
                SO INTEGER,
                HBP INTEGER,
                SH INTEGER,
                SF INTEGER,
                GDP INTEGER,
                SB INTEGER,
                CS INTEGER,
                BA DOUBLE,
                OBP DOUBLE,
                SLG DOUBLE,
                OPS DOUBLE
            )
        """)

        # Updated pitching_stats schema based on Baseball Reference data
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS source_bref__pitching_stats (
                mlbID VARCHAR,
                Name VARCHAR,
                Age INTEGER,
                Team VARCHAR,
                Season INTEGER,
                G INTEGER,
                GS INTEGER,
                W DOUBLE,
                L DOUBLE,
                SV DOUBLE,
                IP DOUBLE,
                H INTEGER,
                R INTEGER,
                ER INTEGER,
                BB INTEGER,
                SO INTEGER,
                HR INTEGER,
                HBP INTEGER,
                ERA DOUBLE,
                AB INTEGER,
                doubles INTEGER,
                triples INTEGER,
                IBB INTEGER,
                GDP INTEGER,
                SF INTEGER,
                SB INTEGER,
                CS INTEGER,
                WHIP DOUBLE,
                SO9 DOUBLE,
                SOW DOUBLE
            )
        """)

    def transform_batting_stats(self, season: int):
        """Transform and load batting stats into DuckDB."""
        file_path = RAW_DIR / f"batting_{season}.parquet"
        if not file_path.exists():
            print(f"No batting data found for {season}")
            return

        self.conn.execute(f"""
            INSERT INTO source_bref__batting_stats
            SELECT
                mlbID,
                Name,
                Age,
                Tm as Team,
                {season} as Season,
                G as Games,
                PA,
                AB,
                R,
                H,
                "2B" as doubles,
                "3B" as triples,
                HR,
                RBI,
                BB,
                IBB,
                SO,
                HBP,
                SH,
                SF,
                GDP,
                SB,
                CS,
                BA,
                OBP,
                SLG,
                OPS
            FROM read_parquet('{file_path}')
        """)

    def transform_pitching_stats(self, season: int):
        """Transform and load pitching stats into DuckDB."""
        file_path = RAW_DIR / f"pitching_{season}.parquet"
        if not file_path.exists():
            print(f"No pitching data found for {season}")
            return

        self.conn.execute(f"""
            INSERT INTO source_bref__pitching_stats
            SELECT
                mlbID,
                Name,
                Age,
                Tm as Team,
                {season} as Season,
                G,
                GS,
                W,
                L,
                SV,
                IP,
                H,
                R,
                ER,
                BB,
                SO,
                HR,
                HBP,
                ERA,
                AB,
                "2B" as doubles,
                "3B" as triples,
                IBB,
                GDP,
                SF,
                SB,
                CS,
                WHIP,
                SO9,
                "SO/W" as SOW
            FROM read_parquet('{file_path}')
        """)

    def transform_roster_assignments(self):
        """Transform and load roster assignments into DuckDB."""
        # Find the most recent roster assignments file
        roster_files = list(RAW_DIR.glob("roster_assignments_*.parquet"))
        if not roster_files:
            print("No roster assignment files found")
            return

        latest_file = max(roster_files, key=lambda x: x.name)

        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS source_fantrax__roster_assignments (
                player_name TEXT,
                team_id TEXT,
                team_name TEXT,
                extract_date DATE
            )
        """)

        # Load into DuckDB
        self.conn.execute(f"""
            DELETE FROM source_fantrax__roster_assignments
            WHERE extract_date = (
                SELECT extract_date
                FROM read_parquet('{latest_file}')
                LIMIT 1
            )
        """)

        self.conn.execute(f"""
            INSERT INTO source_fantrax__roster_assignments
            SELECT
                player_name,
                team_id,
                team_name,
                extract_date
            FROM read_parquet('{latest_file}')
        """)
