"""
Query 2: Get all messages for drivers who retired due to engine failure (True Postgres+Mongo interop)
"""
import pandas as pd
import psycopg2
from pymongo import MongoClient

# Connect to Postgres
pg_conn = psycopg2.connect(
    dbname='F1_Analysis', user='postgres', password='1234', host='localhost'
)
status = pd.read_sql('SELECT "statusId", LOWER(status) as status FROM status', pg_conn)
results = pd.read_sql('SELECT "raceId", "driverId", "statusId" FROM results', pg_conn)

# Identify engine failure statusIds
engine_status_ids = status[status['status'].str.contains('engine')]['statusId'].astype(str).tolist()
engine_failures = set(
    tuple(x)
    for x in results[results['statusId'].astype(str).isin(engine_status_ids)][['raceId', 'driverId']].values
)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
collection = client["F1_Message_Context"]["message_context"]

engine_failure_msgs = []
for (race_id, driver_id) in engine_failures:
    msgs = collection.find({"race_id": int(race_id), "driver_id": int(driver_id)})
    for msg in msgs:
        engine_failure_msgs.append(msg)

# Export results to CSV
if engine_failure_msgs:
    df = pd.DataFrame(engine_failure_msgs)
    df.to_csv('hQ2.csv', index=False)
    print("Exported to hQ2.csv!")
else:
    print("No matching messages found.")