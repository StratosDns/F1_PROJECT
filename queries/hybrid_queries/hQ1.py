"""
Query 1: Find all “Box” messages that correspond to real pit stops

Purpose:
For each radio message about pit stops ("box", "pit for", etc.), check if a real pit stop for the same (race_id, driver_id, lap) exists in the Postgres pit_stops table.
Return all such matched messages, and export to CSV for Tableau or further analysis.

Result: List of radio messages that correspond to actual pit stops (CSV file).

Assumes:
- Radio messages are loaded from MongoDB.
- Pit stops are loaded from pit_stops.csv (or a Postgres query).

Dependencies: pandas, pymongo
"""
import psycopg2
import pandas as pd
from pymongo import MongoClient

# Connect to Postgres
conn = psycopg2.connect(dbname='F1_Analysis', user='postgres', password='1234', host='localhost')
pit_stops = pd.read_sql('SELECT "raceId", "driverId", lap FROM pit_stops', conn)
pit_laps = set((row['raceId'], row['driverId'], row['lap']) for _, row in pit_stops.iterrows())


# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
collection = client["F1_Message_Context"]["message_context"]

# Find all pitstop-related messages in MongoDB
box_msgs = collection.find({
    "$or": [
        {"message_text": {"$regex": "box", "$options": "i"}},
        {"message_text": {"$regex": "pit for", "$options": "i"}},
        {"tags": "pitstop"}
    ]
})

# Filter messages that match a real pit stop
real_box_msgs = []
for msg in box_msgs:
    key = (msg['race_id'], msg['driver_id'], msg['lap'])
    if key in pit_laps:
        real_box_msgs.append(msg)

print(f"Found {len(real_box_msgs)} messages that match real pit stops.")

# Export results to CSV
if real_box_msgs:
    df = pd.DataFrame(real_box_msgs)
    df.to_csv('hQ1.csv', index=False)
    print("Exported to hQ1.csv!")
else:
    print("No matching messages found.")