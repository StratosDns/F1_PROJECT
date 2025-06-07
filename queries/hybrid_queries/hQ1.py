"""
Hybrid Query 1: All radio messages for a driver when they entered the points

- For a given driver, find each lap in any race where they moved from outside the points (position >10)
  to inside the points (position <=10).
- Return all MongoDB radio messages for those (race, lap, driver).
"""

import pandas as pd
from sqlalchemy import create_engine
from pymongo import MongoClient

# --- Setup connections ---
engine = create_engine("postgresql://postgres:1234@localhost:5432/F1_Analysis")
client = MongoClient("mongodb://localhost:27017/")
collection = client["F1_Message_Context"]["message_context"]

driver_id = 44  # e.g., Lewis Hamilton

# --- 1. Get all (raceId, lap, position) for this driver ---
df = pd.read_sql("""
    SELECT "raceId", lap, position
    FROM lap_times
    WHERE "driverId" = %s
    ORDER BY "raceId", lap
""", engine, params=(driver_id,))

# --- 2. Find laps where driver entered the points (crossed from >10 to <=10) ---
df["prev_position"] = df.groupby("raceId")["position"].shift(1).fillna(99)
entered_points = df[(df["prev_position"] > 10) & (df["position"] <= 10)]

# --- 3. Query MongoDB for each (raceId, lap) ---
for _, row in entered_points.iterrows():
    race_id, lap = int(row["raceId"]), int(row["lap"])
    msgs = list(collection.find({"race_id": race_id, "driver_id": driver_id, "lap": lap}))
    for msg in msgs:
        print(f"Race {race_id} Lap {lap}: {msg['message_text']} | Tags: {msg.get('tags', [])}")