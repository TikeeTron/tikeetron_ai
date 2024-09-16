import os
from dotenv import load_dotenv

from langchain_community.document_loaders import JSONLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pymongo import MongoClient

load_dotenv()

DB_NAME = os.getenv("MONGO_DB_NAME")
COLLECTION_NAME = os.getenv("MONGO_COLLECTION_EVENTS")
client = MongoClient(os.getenv("MONGO_URI"))
db = client[DB_NAME]
MONGODB_COLLECTION = db[COLLECTION_NAME]


# Metadata extraction function
def metadata_func(record: dict, metadata: dict) -> dict:
    tickets = record.get("tickets")

    metadata["id"] = record.get("id")
    metadata["name"] = record.get("name")
    metadata["category"] = record.get("category")
    metadata["start_date"] = record.get("start_date")
    metadata["end_date"] = record.get("end_date")
    metadata["tickets"] = {
        "id": [ticket.get("id") for ticket in tickets],
        "name": [ticket.get("name") for ticket in tickets],
        "price": [ticket.get("price") for ticket in tickets],
        "quantity": [ticket.get("quantity") for ticket in tickets],
        "start_date": [ticket.get("start_date") for ticket in tickets],
        "end_date": [ticket.get("end_date") for ticket in tickets],
    }

    return metadata


## Load Data
loader = JSONLoader(
    file_path="./app/data/mock_events.json",
    jq_schema=".[]",
    text_content=False,
    is_content_key_jq_parsable=True,
    content_key=".content",
    metadata_func=metadata_func,
)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=2500, chunk_overlap=2000)
all_splits = text_splitter.split_documents(loader.load())

vectorstore = MongoDBAtlasVectorSearch.from_documents(
    documents=all_splits,
    embedding=HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2", model_kwargs={"device": "cpu"}
    ),
    collection=MONGODB_COLLECTION,
    index_name=os.getenv("MONGO_VECTOR_INDEX_EVENTS"),
)
