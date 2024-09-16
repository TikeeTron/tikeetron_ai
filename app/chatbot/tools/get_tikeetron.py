import os

from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain_huggingface import HuggingFaceEmbeddings

from langchain.tools.retriever import create_retriever_tool

vectorstore = MongoDBAtlasVectorSearch.from_connection_string(
    os.environ["MONGO_URI"],
    os.environ["MONGO_DB_NAME"] + "." + os.environ["MONGO_COLLECTION_TIKEETRON"],
    HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2", model_kwargs={"device": "cpu"}
    ),
    index_name=os.environ["MONGO_VECTOR_INDEX_TIKEETRON"],
)

retriever = vectorstore.as_retriever()

get_tikeetron_tool = create_retriever_tool(
    retriever=retriever,
    name="Get to know Tikeetron",
    description="use this tool to get a brief overview of Tikeetron, this tool is used vector search to find the most similar document to the query",
)
