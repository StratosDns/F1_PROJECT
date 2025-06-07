
# Finding races with the most documented circuits using MongoDB and Postgres

import psycopg2
import pandas as pd
from pymongo import MongoClient

# 1. Count messages per race_id from MongoDB
client = MongoClient("mongodb://localhost:27017/")
collection = client["F1_Message_Context"]["message_context"]

pipeline = [
    {"$group": {"_id": "$race_id", "message_count": {"$sum": 1}}}
]
race_msg_counts = list(collection.aggregate(pipeline))
race_df = pd.DataFrame(race_msg_counts).rename(columns={"_id": "raceId"})

# 2. Map raceId to circuitId via Postgres
pg_conn = psycopg2.connect(
    dbname='F1_Analysis', user='postgres', password='1234', host='localhost'
)
races = pd.read_sql('SELECT "raceId", "circuitId", "name", "year" FROM races', pg_conn)

# 3. Merge and sum over circuitId
merged = pd.merge(race_df, races, on="raceId")
circuit_msg_counts = merged.groupby(["circuitId"]).agg(
    total_msgs=pd.NamedAgg(column="message_count", aggfunc="sum"),
    races=pd.NamedAgg(column="raceId", aggfunc="count")
).reset_index()

# 4. Get the top circuit(s)
top = circuit_msg_counts.sort_values("total_msgs", ascending=False).iloc[0]

# 5. Get circuit info (name, location) if you want
circuits = pd.read_sql('SELECT * FROM circuits', pg_conn)
circuit_info = circuits[circuits['circuitId'] == top['circuitId']].iloc[0]

print(f"Most documented circuit: {circuit_info['name']} ({circuit_info['location']}, {circuit_info['country']})")
print(f"Circuit ID: {top['circuitId']}")
print(f"Total messages: {top['total_msgs']}")
print(f"Races hosted: {top['races']}")