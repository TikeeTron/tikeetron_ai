import os

from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import format_document, PromptTemplate
from langchain_core.runnables import RunnablePassthrough
import requests

from app.chatbot.prompt.base_prompt import DOCUMENT_PROMPT

from dotenv import load_dotenv

load_dotenv()

BASE_API_URL = os.getenv("BASE_API_URL")

session = requests.Session()
session.auth = (os.getenv("HTTP_BASIC_USER"), os.getenv("HTTP_BASIC_PASSWORD"))


system_prompt = """
Use the event data below to answer the user's question. Show id, name, and category. If no data is available, say, "No events found.". Do not ask for more clarification unless needed.

## Question: 
{question}

## Context: 
{context}
"""

# prompt = ChatPromptTemplate.from_messages([("system", system_prompt)])
prompt = PromptTemplate(
    template=system_prompt,
    input_variables=["context", "question"],
)

vectorstore = MongoDBAtlasVectorSearch.from_connection_string(
    os.environ["MONGO_URI"],
    os.environ["MONGO_DB_NAME"] + "." + os.environ["MONGO_COLLECTION_EVENTS"],
    HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
    ),
    index_name=os.environ["MONGO_VECTOR_INDEX_EVENTS"],
)

retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={
        "k": 2,
        "filters": {
            "$or": [
                {"start_date": {"$gte": "now"}},
                {"end_date": {"$gte": "now"}},
            ]
        },
    },
)

llm = ChatGroq(
    model="llama3-70b-8192",
    temperature=0,
    max_retries=1,
    api_key=os.getenv("GROQ_API_KEY"),
    verbose=True,
)


def _combine_documents(
    docs, document_prompt=DOCUMENT_PROMPT, document_separator="\n\n"
):
    doc_strings = [format_document(doc, document_prompt) for doc in docs]
    print(document_separator.join(doc_strings))
    return document_separator.join(doc_strings)


rag_chain = (
    {
        "context": retriever | _combine_documents,
        "question": RunnablePassthrough(),
    }
    | prompt
    | llm
    | StrOutputParser()
)

get_current_event_tool = rag_chain.as_tool(
    name="get_events",
    description="use this tool to get the events, pass the question to the parameter",
)


def get_events_by_ids(
    event_ids: list,
):
    """use this tool to get the events by the event ids"""

    if event_ids is None or len(event_ids) == 0:
        return []

    request_session = session.get(
        f"{BASE_API_URL}/v1/events",
        params={
            "eventIds[]": event_ids,
        },
    )
    events = request_session.json()["data"]

    print(events)

    return events
