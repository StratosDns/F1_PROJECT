import psycopg2
import pandas as pd

race_id = 540  # Replace with actual race_id

pg_conn = psycopg2.connect(
    dbname='F1_Analysis', user='postgres', password='1234', host='localhost'
)
race = pd.read_sql('SELECT "raceId", "year", "name", "circuitId" FROM races WHERE "raceId" = %s', pg_conn, params=[race_id])
if not race.empty:
    print(f"Race: {race.iloc[0]['name']} ({race.iloc[0]['year']}), circuitId: {race.iloc[0]['circuitId']}")
else:
    print("Race not found.")