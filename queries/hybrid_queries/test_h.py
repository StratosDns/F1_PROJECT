import pandas as pd
from sqlalchemy import create_engine
from pymongo import MongoClient

# --- Connect to Postgres ---
engine = create_engine("postgresql://postgres:1234@localhost:5432/F1_Analysis")

# Example: "Find all radio messages when driver entered the points"
driver_id = 44

# Get all (raceId, lap, position) for this driver
df = pd.read_sql("""
    SELECT "raceId", lap, position
    FROM lap_times
    WHERE "driverId" = %s
    ORDER BY "raceId", lap
""", engine, params=(driver_id,))

# Find laps where driver entered points (position crosses 10th place)
df["prev_position"] = df.groupby("raceId")["position"].shift(1).fillna(99)
entered_points = df[(df["prev_position"] > 10) & (df["position"] <= 10)]

# --- Connect to MongoDB ---
client = MongoClient("mongodb://localhost:27017/")
collection = client["F1_Message_Context"]["message_context"]

# Query MongoDB for each (raceId, lap)

for _, row in entered_points.iterrows():
    race_id, lap = int(row["raceId"]), int(row["lap"])
    msgs = list(collection.find({"race_id": race_id, "driver_id": driver_id, "lap": lap}))
    for msg in msgs:
        print(f"Race {race_id} Lap {lap}: {msg['message_text']} | Tags: {msg['tags']}")