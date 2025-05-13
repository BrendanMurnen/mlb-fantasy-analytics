import duckdb
from pathlib import Path
from src.config.config import DB_PATH, PROCESSED_DIR

class StagingTablePublisher:
    def __init__(self):
        self.conn = duckdb.connect(str(DB_PATH))
        self.staging_queries_dir = Path(__file__).parent.parent / "src" / "data" / "staging_queries"

    def read_sql_file(self, file_path: Path) -> str:
        """Read the contents of a SQL file."""
        with open(file_path, 'r') as f:
            return f.read()

    def get_table_name_from_file(self, file_path: Path) -> str:
        """Extract table name from the SQL file name."""
        return file_path.stem

    def publish_staging_tables(self):
        """Process all SQL files and publish results to parquet files."""
        sql_files = list(self.staging_queries_dir.glob("*.sql"))

        if not sql_files:
            print("No SQL files found in the staging queries directory.")
            return

        for sql_file in sql_files:
            table_name = self.get_table_name_from_file(sql_file)
            print(f"Processing {table_name}...")

            # Read and execute the SQL query
            sql_query = self.read_sql_file(sql_file)

            # Create a view with the query results
            self.conn.execute(f"CREATE OR REPLACE VIEW {table_name}_view AS {sql_query}")

            # Create or replace the table
            self.conn.execute(f"DROP TABLE IF EXISTS {table_name}")
            self.conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM {table_name}_view")

            # Export to parquet
            output_path = PROCESSED_DIR / f"{table_name}.parquet"
            self.conn.execute(f"COPY {table_name} TO '{output_path}' (FORMAT 'parquet')")

            print(f"Published {table_name} to {output_path}")

def main():
    print("Starting staging table publication...")
    publisher = StagingTablePublisher()
    publisher.publish_staging_tables()
    print("\nStaging table publication completed successfully!")

if __name__ == "__main__":
    main()
