
#Ok let's now create a query that will output the total number of messages documented for every different circuit_id and which team has sent the most messages in each circuit

import psycopg2
import pandas as pd
from pymongo import MongoClient
from collections import defaultdict, Counter

# Connect to Postgres
pg_conn = psycopg2.connect(
    dbname='F1_Analysis', user='postgres', password='1234', host='localhost'
)

# Get raceId, circuitId for all races
races = pd.read_sql('SELECT "raceId", "circuitId" FROM races', pg_conn)

# Get driverId, constructorId, raceId for all results
results = pd.read_sql('SELECT "raceId", "driverId", "constructorId" FROM results', pg_conn)

# Get constructorId, name mapping
constructors = pd.read_sql('SELECT "constructorId", "name" FROM constructors', pg_conn)
constructor_names = {row['constructorId']: row['name'] for _, row in constructors.iterrows()}

# Get circuitId, name mapping
circuits = pd.read_sql('SELECT "circuitId", "name" FROM circuits', pg_conn)
circuit_names = {row['circuitId']: row['name'] for _, row in circuits.iterrows()}

# Build a mapping: (raceId, driverId) -> team name
race_driver_to_team = {(row['raceId'], row['driverId']): constructor_names.get(row['constructorId'], f"constructor_{row['constructorId']}") for _, row in results.iterrows()}

# Map raceId -> circuitId
race_to_circuit = {row['raceId']: row['circuitId'] for _, row in races.iterrows()}

# Connect to MongoDB and get all messages
client = MongoClient("mongodb://localhost:27017/")
collection = client["F1_Message_Context"]["message_context"]
all_msgs = collection.find({})

# For each circuit, keep a list of all teams' message counts
circuit_total_msgs = defaultdict(int)
circuit_team_counts = defaultdict(lambda: Counter())

# Process each message
for msg in all_msgs:
    race_id = msg.get('race_id')
    driver_id = msg.get('driver_id')
    if race_id not in race_to_circuit:
        continue
    circuit_id = race_to_circuit[race_id]
    team = race_driver_to_team.get((race_id, driver_id), "Unknown")
    circuit_total_msgs[circuit_id] += 1
    circuit_team_counts[circuit_id][team] += 1

# Prepare results
rows = []
for circuit_id, total_msgs in circuit_total_msgs.items():
    team_counts = circuit_team_counts[circuit_id]
    if team_counts:
        top_team, top_count = team_counts.most_common(1)[0]
    else:
        top_team, top_count = "None", 0
    circuit_name = circuit_names.get(circuit_id, "Unknown")
    rows.append({
        "circuitId": circuit_id,
        "circuit_name": circuit_name,
        "total_msgs": total_msgs,
        "top_team": top_team,
        "top_team_msgs": top_count
    })

df = pd.DataFrame(rows)
df.to_csv("circuit_message_stats_with_name.csv", index=False)
print("Exported to circuit_message_stats_with_name.csv!")