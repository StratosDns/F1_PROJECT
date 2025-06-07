"""
Hybrid Query 2: All radio messages in the 3 laps after a pit stop (for a driver/race)

- For a given driver (and optionally a specific race), find all their pit stops.
- For each pit stop, fetch all MongoDB radio messages on laps lap+1, lap+2, lap+3.
"""

import pandas as pd
from sqlalchemy import create_engine
from pymongo import MongoClient

engine = create_engine("postgresql://postgres:1234@localhost:5432/F1_Analysis")
client = MongoClient("mongodb://localhost:27017/")
collection = client["F1_Message_Context"]["message_context"]

driver_id = 44

# --- 1. Get all pit stops for driver ---
df = pd.read_sql("""
    SELECT "raceId", stop, lap
    FROM pit_stops
    WHERE "driverId" = %s
    ORDER BY "raceId", lap
""", engine, params=(driver_id,))

# --- 2. For each pit stop, get messages on laps lap+1, lap+2, lap+3 ---
for _, row in df.iterrows():
    race_id, pit_lap = int(row["raceId"]), int(row["lap"])
    for lap in [pit_lap+1, pit_lap+2, pit_lap+3]:
        msgs = list(collection.find({"race_id": race_id, "driver_id": driver_id, "lap": lap}))
        for msg in msgs:
            print(f"Race {race_id} Lap {lap}: {msg['message_text']} | Tags: {msg.get('tags', [])}")