"""
Query 3: Messages sent right after a pit stop

Purpose:
For each pit stop (race_id, driver_id, lap), get all radio messages for the same driver/race
on the next 2 laps (lap+1, lap+2). Export the result to a CSV for use in Tableau or further analysis.

Result: List of messages sent immediately after pit stops (CSV output).

Assumes:
- pit_stops.csv in Postgres or CSV.
- Radio messages in MongoDB.

Dependencies: pandas, pymongo
"""
import pandas as pd
import psycopg2
from pymongo import MongoClient

# Connect to Postgres
pg_conn = psycopg2.connect(
    dbname='F1_Analysis', user='postgres', password='1234', host='localhost'
)
pit_stops = pd.read_sql('SELECT "raceId", "driverId", lap FROM pit_stops', pg_conn)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
collection = client["F1_Message_Context"]["message_context"]

post_pit_msgs = []
for _, row in pit_stops.iterrows():
    race_id = int(row['raceId'])
    driver_id = int(row['driverId'])
    pit_lap = int(row['lap'])
    for lap in [pit_lap + 1, pit_lap + 2]:
        msgs = collection.find({"race_id": race_id, "driver_id": driver_id, "lap": lap})
        for msg in msgs:
            post_pit_msgs.append(msg)

# Export results to CSV
if post_pit_msgs:
    df = pd.DataFrame(post_pit_msgs)
    df.to_csv('hQ3.csv', index=False)
    print("Exported to hQ3.csv!")
else:
    print("No matching messages found.")