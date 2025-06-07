from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["F1_Message_Context"]
collection = db["message_context"]

# Example: pitstop messages for Hamilton (driver_id 44) in race 55
messages = collection.find({"race_id": 55, "driver_id": 44, "tags": "pitstop"})
for msg in messages:
    print(f"Lap: {msg['lap']} -> Message: {msg['message_text']} | Tags: {msg['tags']}")

print("Query complete.")