import json
from pymongo import MongoClient

# Adjust file path and MongoDB connection as needed
with open('C:/F1_Project/data/mongo/data_mongo_driver_radio_messages.json', 'r') as f:
    messages = json.load(f)

client = MongoClient('mongodb://localhost:27017/')
db = client['F1_Message_Context']
collection = db['message_context']

# Insert all messages (optionally, clear collection first)
collection.delete_many({})
collection.insert_many(messages)

print(f"Inserted {len(messages)} messages into MongoDB.")