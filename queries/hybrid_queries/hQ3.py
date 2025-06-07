"""
Hybrid Query 3: Find the lap with the most radio messages for a driver in a race

- For a given driver and race, find which lap in MongoDB has the most messages.
- Display the position of the driver on that lap (from Postgres).
"""

import pandas as pd
from sqlalchemy import create_engine
from pymongo import MongoClient
from collections import Counter

engine = create_engine("postgresql://postgres:1234@localhost:5432/F1_Analysis")
client = MongoClient("mongodb://localhost:27017/")
collection = client["F1_Message_Context"]["message_context"]

race_id = 165
driver_id = 44

# --- 1. Get all messages for race/driver ---
msgs = list(collection.find({"race_id": race_id, "driver_id": driver_id}))
lap_counts = Counter(msg['lap'] for msg in msgs)
if not lap_counts:
    print("No messages found.")
else:
    lap_most = lap_counts.most_common(1)[0][0]
    print(f"Lap with most messages: {lap_most}")

    # --- 2. Get driver's position on that lap ---
    engine = create_engine("postgresql://postgres:1234@localhost:5432/F1_Analysis")
    sql = 'SELECT position FROM lap_times WHERE "raceId" = %s AND "driverId" = %s AND lap = %s'
    pos = pd.read_sql(sql, engine, params=(race_id, driver_id, lap_most))
    print(pos)

    # --- 3. Print messages from that lap ---
    for msg in filter(lambda m: m['lap'] == lap_most, msgs):
        print(f"Lap {lap_most}: {msg['message_text']} | Tags: {msg.get('tags', [])}")