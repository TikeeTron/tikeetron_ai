import os

from dotenv import load_dotenv

from urllib.parse import urljoin

from pymongo import MongoClient
from bson.json_util import dumps

from crud import insert_event_vector, update_event_vector

load_dotenv()

DB_NAME = os.getenv("MONGO_API_DB_NAME")
COLLECTION_NAME = "events"
client = MongoClient(os.getenv("MONGO_URI"))
db = client[DB_NAME]
MONGODB_COLLECTION = db[COLLECTION_NAME]

change_stream = MONGODB_COLLECTION.watch()
for change in change_stream:
    if change["operationType"] == "insert":
        insert_event_vector(change["fullDocument"])
    elif change["operationType"] == "update":
        print(change["documentKey"]["_id"])
        update_event_vector(
            change["documentKey"]["_id"],
            change["updateDescription"]["updatedFields"],
        )
    print(dumps(change))
