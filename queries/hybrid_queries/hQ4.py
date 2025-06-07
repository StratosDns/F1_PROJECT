"""
Query 4: Get all ‘Final Lap’ messages and driver’s actual position on that lap

Purpose:
For every radio message with tag or text 'final_lap', return the driver’s position on that lap from lap_times.csv.
Export the result as a CSV for Tableau or further analysis.

Result: List of (race_id, driver_id, lap, message_text, position) for each final lap message (CSV output).

Assumes:
- MongoDB messages.
- lap_times.csv or Postgres lap_times table.

Dependencies: pandas, pymongo, psycopg2
"""
import psycopg2
import pandas as pd
from pymongo import MongoClient

# Connect to Postgres
pg_conn = psycopg2.connect(
    dbname='F1_Analysis', user='postgres', password='1234', host='localhost'
)
lap_times = pd.read_sql('SELECT "raceId", "driverId", lap, position FROM lap_times', pg_conn)
lap_times_lookup = {(row['raceId'], row['driverId'], row['lap']): row['position'] for _, row in lap_times.iterrows()}

client = MongoClient("mongodb://localhost:27017/")
collection = client["F1_Message_Context"]["message_context"]

final_lap_msgs = collection.find({
    "$or": [
        {"message_text": {"$regex": "final lap", "$options": "i"}},
        {"tags": "final_lap"}
    ]
})

results = []
for msg in final_lap_msgs:
    key = (msg['race_id'], msg['driver_id'], msg['lap'])
    position = lap_times_lookup.get(key, None)
    results.append({
        'race_id': msg['race_id'],
        'driver_id': msg['driver_id'],
        'lap': msg['lap'],
        'message_text': msg['message_text'],
        'position': position
    })

print(f"Found {len(results)} final lap messages with position info.")

# Export to CSV
if results:
    df = pd.DataFrame(results)
    df.to_csv('hQ4.csv', index=False)
    print("Exported to hQ4.csv!")
else:
    print("No matching messages found.")