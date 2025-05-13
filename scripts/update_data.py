# scripts/update_data.py
from src.data.extraction import MLBDataExtractor
from src.data.transformation import MLBDataTransformer
from src.config.config import SEASONS_TO_COLLECT

def main():
    # Extract data
    print("Starting data extraction...")
    extractor = MLBDataExtractor()
    extractor.extract_all_stats()

    # Transform and load data
    print("\nStarting data transformation...")
    transformer = MLBDataTransformer()
    transformer.setup_database()

    # Transform roster assignments
    transformer.transform_roster_assignments()

    # Transform stats
    for season in SEASONS_TO_COLLECT:
        transformer.transform_batting_stats(season)
        transformer.transform_pitching_stats(season)

    print("\nData pipeline completed successfully!")

if __name__ == "__main__":
    main()
