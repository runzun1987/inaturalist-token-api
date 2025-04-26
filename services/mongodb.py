from http.client import HTTPException

from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId

import os
from dotenv import load_dotenv

load_dotenv()

REQUIRED_ENV_VARS = [
    "MONGO_DB_URL"

]

for var in REQUIRED_ENV_VARS:
    value = os.getenv(var)
    if not value:
        raise ValueError(f"Missing required environment variable: {var}")
    os.environ[var] = value


# Initialize MongoDB client
try:
    client = MongoClient(os.getenv("MONGO_DB_URL"))
    # Force a connection by listing databases
    client.list_database_names()
    print("✅ MongoDB connection successful.")
except Exception as e:
    print(os.getenv("MONGO_DB_URL"))
    print("❌ Failed to connect to MongoDB:", e)
    print(os.getenv("MONGO_DB_URL"))
    raise e  # Stop the app if MongoDB fails

print(os.getenv("MONGO_DB_URL"))

# client = MongoClient(os.getenv("MONGO_DB_URL"))
db = client["inaturalist-token"]
tokens_collection = db["tokens"]




def post_token_mongodb(token):
    token_data = {
        "value": token.value,
        "timestamp": datetime.utcnow()
    }
    result = tokens_collection.insert_one(token_data)
    return {"message": "Token saved", "id": str(result.inserted_id)}


def get_token_mongodb():
    latest_token = tokens_collection.find_one(sort=[("timestamp", -1)])
    if not latest_token:
        raise HTTPException()
    return {
        "token": latest_token["value"],
        "timestamp": latest_token["timestamp"]
    }