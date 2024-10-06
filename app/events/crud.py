import json
import os

from bson import json_util
from dotenv import load_dotenv

from bson import ObjectId
from langchain_core import documents
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain_huggingface import HuggingFaceEmbeddings
from pymongo import MongoClient

load_dotenv()

DB_NAME = os.getenv("MONGO_API_DB_NAME")
COLLECTION_NAME = "events"
client = MongoClient(os.getenv("MONGO_URI"))
db = client[DB_NAME]
eventCollections = db[COLLECTION_NAME]

vectorstore = MongoDBAtlasVectorSearch.from_connection_string(
    os.environ["MONGO_URI"],
    os.environ["MONGO_DB_NAME"] + "." + os.environ["MONGO_COLLECTION_EVENTS"],
    HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
    ),
    index_name=os.environ["MONGO_VECTOR_INDEX_EVENTS"],
)


def format_content(event: dict):
    """
    Format the event content for display in the chatbot.
    """
    return {
        "id": event.get("_id"),
        "name": event.get("name"),
        "description": event.get("description"),
        "category": event.get("category"),
    }


def insert_event_vector(event: dict):
    """
    Insert the event vector into the MongoDB Atlas database.
    """
    document = documents.Document(
        page_content=str(format_content(event)),
        metadata=event,
    )

    vectorstore.add_documents(
        documents=[document],
        ids=[event["_id"]],
    )
    return event


def update_event_vector(id: ObjectId, updatedFields):
    """
    Update the event vector in the MongoDB Atlas database.
    """

    event = eventCollections.find_one({"_id": id})
    updated_event = {**event, **updatedFields}

    vectorstore._collection.delete_one({"_id": id})

    return insert_event_vector(updated_event)


def get_event_datas(events):
    """
    Get the event data from the MongoDB Atlas database.
    """
    event_datas = []
    event_ids = [ObjectId(event.id) for event in events]

    for event in eventCollections.find({"_id": {"$in": event_ids}}):
        event_datas.append(event)

    return json.loads(json_util.dumps(event_datas))
