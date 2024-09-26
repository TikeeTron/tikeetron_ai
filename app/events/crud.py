import os

from bson import ObjectId
from langchain_core import documents
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain_huggingface import HuggingFaceEmbeddings

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

    return vectorstore._collection.update_one(
        {"_id": id},
        {"$set": updatedFields},
    )
