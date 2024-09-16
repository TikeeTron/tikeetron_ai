import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pymongo import MongoClient

MONGO_URI = os.environ["MONGO_URI"]

DB_NAME = os.environ["MONGO_DB_NAME"]
COLLECTION_NAME = os.environ["MONGO_COLLECTION_TIKEETRON"]
ATLAS_VECTOR_SEARCH_INDEX_NAME = os.environ["MONGO_VECTOR_INDEX_TIKEETRON"]

EMBEDDING_FIELD_NAME = "embedding"
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
MONGODB_COLLECTION = db[COLLECTION_NAME]

if __name__ == "__main__":
    loader = PyPDFLoader("app/data/tikeetron.pdf")
    data = loader.load()

    # Split docs
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    docs = text_splitter.split_documents(data)

    # Insert the documents in MongoDB Atlas Vector Search
    _ = MongoDBAtlasVectorSearch.from_documents(
        documents=docs,
        embedding=HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2", model_kwargs={"device": "cpu"}
        ),
        collection=MONGODB_COLLECTION,
        index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
    )
