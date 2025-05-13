# MLB Fantasy Analytics

A Python project for statistical analysis of MLB players and fantasy baseball roster optimization. Right now it's mostly data cleaning + transformation's from [Fantrax API](https://fantraxapi.metamanager.wiki/en/stable/intro.html) and [Pro Baseball Reference, via PyBaseball](https://github.com/jldbc/pybaseball/tree/master)

## Setup
1. Create virtual environment: `python -m venv venv`
2. Activate virtual environment: `source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`

## Project Structure
```
mlb-fantasy-analytics/
│
├── .env                      # Environment variables (API keys, credentials)
├── .gitignore               # Git ignore file
├── README.md                # Project documentation
├── requirements.txt         # Python dependencies
├── pyproject.toml          # Project metadata and build configuration
│
├── data/                    # Data directory (gitignored)
│   ├── raw/                # Raw data from pybaseball and fantrax
│   ├── processed/          # Cleaned and transformed data
│   └── duckdb/            # DuckDB database files
│
├── notebooks/              # Jupyter notebooks for exploration
│   └── exploration/       # Exploratory analysis notebooks
│
├── src/                    # Production code
│   ├── __init__.py
│   ├── config/           # Configuration files
│   │   └── config.py
│   │
│   ├── data/             # Data processing modules
│   │   ├── extraction.py   # Data extraction from APIs
│   │   ├── transformation.py # Data cleaning and transformation
│   │   └── loading.py      # Loading data into DuckDB
│   │
│   ├── analysis/         # Analysis modules
│   │   ├── stats.py      # Statistical analysis functions
│   │   └── optimization.py # Roster optimization logic
│   │
│   ├── api/             # API related code
│   │   ├── pybaseball_client.py
│   │   └── fantrax_client.py
│   │
│   └── visualization/   # Visualization modules
│       └── plots.py
│
├── tests/               # Test directory
│   ├── __init__.py
│   ├── test_data.py
│   └── test_analysis.py
│
├── app/                # Frontend application
│   ├── static/
│   ├── templates/
│   └── main.py        # Streamlit/Dash/Flask app
│
└── scripts/           # Utility scripts
    ├── update_data.py
    └── generate_reports.py
```
