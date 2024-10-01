import os

from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage


from app.chatbot.model.response_model import AgentState, EventResponse, EventsResponse
from app.chatbot.tools.get_tikeetron import get_tikeetron_tool
from app.chatbot.tools.get_my_tickets import GetMyTicketsTool
from app.chatbot.tools.get_current_events import get_current_event_tool
from app.events.crud import get_event_datas

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
    max_retries=1,
    api_key=os.getenv("GROQ_API_KEY"),
    verbose=True,
)

model_with_structured_output = llm.with_structured_output(EventsResponse)
model_with_tools = llm.bind_tools(tools)


# Define the function that calls the model
def call_model(state: AgentState):
    response = model_with_tools.invoke(state["messages"])
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}


# Define the function that responds to the user
def respond(state: AgentState):
    response = model_with_structured_output.invoke(
        [HumanMessage(content=state["messages"][-2].content)]
    )

    if response.events and response.events[0].id:
        return {
            "events": response.events,
            "message": "Here are the events I found:",
        }
    else:
        return {
            "events": [],
            "message": "No events found.",
        }


# Define the function that determines whether to continue or not
def should_continue(state: AgentState):
    messages = state["messages"]
    last_message = messages[-1]
    # If there is no function call, then we respond to the user
    if not last_message.tool_calls:
        return "respond"
    # Otherwise if there is, we continue
    else:
        return "continue"


# Define a new graph
workflow = StateGraph(AgentState)

# Define the two nodes we will cycle between
workflow.add_node("agent", call_model)
workflow.add_node("respond", respond)
workflow.add_node("tools", ToolNode(tools))

# Set the entrypoint as `agent`
# This means that this node is the first one called
workflow.set_entry_point("agent")

# We now add a conditional edge
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "tools",
        "respond": "respond",
    },
)

workflow.add_edge("tools", "agent")
workflow.add_edge("respond", END)
graph = workflow.compile()


def get_events(events: list):
    return get_event_datas(events) if events else []


def ask_agent(messages):
    response = graph.invoke(
        input={
            "messages": [
                (
                    "system",
                    """You are Tikeetron Bot. Follow these rules:
1. For event-related questions (e.g., "What events are happening?"), call `get_events`, retrieve the event ID, name, and category, and return the event name along with a brief description. Ensure your response is based on the retrieved event data only.
2. For ticket/transaction inquiries, call `get_my_tickets`.
3. For general queries (NFTs or Tikeetron info), call `get_to_know_tikeetron`.

Present the event data clearly in your response and do not ask for clarification unless absolutely necessary. Ensure all responses are based on the provided data without introducing any fabricated information.
                    """.strip(
                        "\n"
                    ),
                ),
                (
                    "human",
                    messages,
                ),
            ],
        },
        debug=True,
    )

    print(response)

    message = response["messages"][-1]
    if message != None:
        return {
            "message": message.content,
            "events": get_events(response["events"]),
        }
    else:
        return {
            "message": "I'm sorry, I don't have an answer for that.",
        }
