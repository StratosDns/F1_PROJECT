from pymongo import MongoClient
import pandas as pd

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
collection = client["F1_Message_Context"]["message_context"]

# Load all unique (race_id, driver_id) from Mongo
mongo_pairs = set((int(m["race_id"]), int(m["driver_id"])) for m in collection.find({}, {"race_id":1, "driver_id":1}))

# Load all valid pairs from Postgres
results = pd.read_csv('../data/postgres/results.csv')
sql_pairs = set((int(row.raceId), int(row.driverId)) for i, row in results.iterrows())

# Find inconsistencies
missing_in_sql = mongo_pairs - sql_pairs
missing_in_mongo = sql_pairs - mongo_pairs

print("Pairs in Mongo but not in SQL:", missing_in_sql)
print("Pairs in SQL but not in Mongo (should be fine):", missing_in_mongo)