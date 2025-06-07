"""
Query 6: Most frequent message types per team

Purpose:
For each constructor/team, count the occurrence of each message_type in radio messages.
Export this as a CSV suitable for Tableau or further analysis.

Result: For each team, a breakdown of message_type counts (CSV output).

Assumes:
- MongoDB messages.
- results.csv for driverId -> constructorId mapping.
- constructors.csv for team names.

Dependencies: pandas, pymongo, psycopg2
"""

import pandas as pd
from pymongo import MongoClient
import psycopg2
from collections import defaultdict

# Connect to Postgres
pg_conn = psycopg2.connect(
    dbname='F1_Analysis', user='postgres', password='1234', host='localhost'
)
results = pd.read_sql('SELECT "raceId", "driverId", "constructorId" FROM results', pg_conn)
constructors = pd.read_sql('SELECT "constructorId", name FROM constructors', pg_conn)

# Build mappings
driver_to_constructor = {(row['raceId'], row['driverId']): row['constructorId'] for _, row in results.iterrows()}
constructor_names = {row['constructorId']: row['name'] for _, row in constructors.iterrows()}

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
collection = client["F1_Message_Context"]["message_context"]

# Aggregate message types per team
team_msg_types = defaultdict(lambda: defaultdict(int))

all_msgs = collection.find({})
for msg in all_msgs:
    key = (msg['race_id'], msg['driver_id'])
    constructor_id = driver_to_constructor.get(key)
    if constructor_id:
        team = constructor_names.get(constructor_id, f"constructor_{constructor_id}")
        team_msg_types[team][msg['message_type']] += 1

# Prepare data for export
rows = []
for team, msg_types in team_msg_types.items():
    for msg_type, count in msg_types.items():
        rows.append({
            'team': team,
            'message_type': msg_type,
            'count': count
        })

# Export to CSV
df = pd.DataFrame(rows)
df.to_csv('hQ5.csv', index=False)
print("Exported to hQ5.csv!")

# Print breakdown for reference
for team, msg_types in team_msg_types.items():
    print(f"Team: {team}")
    for msg_type, count in msg_types.items():
        print(f"  {msg_type}: {count}")
    print()