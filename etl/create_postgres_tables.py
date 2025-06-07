import pandas as pd
from sqlalchemy import create_engine

# Set up your connection string (update with your DB credentials)
engine = create_engine('postgresql://postgres:1234@localhost:5432/F1_Analysis')

# List of CSVs and table names
csv_files = {
    "drivers": "../data/postgres/drivers.csv",
    "races": "../data/postgres/races.csv",
    "results": "../data/postgres/results.csv",
    "constructors": "../data/postgres/constructors.csv",
    "pit_stops": "../data/postgres/pit_stops.csv",
    "lap_times": "../data/postgres/lap_times.csv"
    # Add more as needed
}

for table, path in csv_files.items():
    df = pd.read_csv(path)
    df.to_sql(table, engine, if_exists='replace', index=False)  # Creates table if not exists
    print(f"Loaded {table} from {path}")