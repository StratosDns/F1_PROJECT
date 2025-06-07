import psycopg2
from pymongo import MongoClient

# PostgreSQL
pg_conn = psycopg2.connect(
    dbname='F1_Analysis',
    user='postgres',           # Update if using a different user
    password='1234',  # Fill in your actual password
    host='localhost',
    port=5432
)
print("Connected to PostgreSQL!")

# MongoDB
mongo_client = MongoClient('mongodb://localhost:27017/')
mongo_db = mongo_client['F1_Message_Context']
print("Connected to MongoDB!")