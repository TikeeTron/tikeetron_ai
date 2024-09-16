import os

# from langchain import hub
from dotenv import load_dotenv

# from langchain.agents import  AgentExecutor
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent

from app.chatbot.tools.get_tikeetron import get_tikeetron_tool
from app.chatbot.tools.get_my_tickets import GetMyTicketsTool
from app.chatbot.tools.get_current_events import get_current_event_tool

load_dotenv()

tools = [
    GetMyTicketsTool(),
    get_current_event_tool,
    get_tikeetron_tool,
]

llm = ChatGroq(
    model="llama3-70b-8192",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=os.getenv("GROQ_API_KEY"),
    verbose=True,
)

agent = create_react_agent(
    llm,
    tools,
)


def ask_agent(messages):
    response = agent.invoke(
        {
            "messages": [
                (
                    "system",
                    "You are the Tikeetron Bot, designed to assist users with questions about events. Ensure that your responses are accurate and based on the provided passages.",
                ),
                (
                    "human",
                    messages,
                ),
            ],
        },
    )

    message = response["messages"][-1]
    if message != None:
        return message.content
    else:
        return "No response"
