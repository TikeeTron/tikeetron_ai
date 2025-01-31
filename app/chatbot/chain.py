import os

from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage


from app.chatbot.model.response_model import AgentState, ToolResponse
from app.chatbot.tools.get_my_tickets import get_my_tickets_tool, get_tickets_by_ids
from app.chatbot.tools.get_tikeetron import get_tikeetron_tool
from app.chatbot.tools.get_current_events import (
    get_current_event_tool,
    get_events_by_ids,
)
from app.events.crud import get_event_datas

load_dotenv()

tools = [
    get_my_tickets_tool,
    get_current_event_tool,
    get_tikeetron_tool,
]

llm = ChatGroq(
    model="llama-3.2-90b-text-preview",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=1,
    api_key=os.getenv("GROQ_API_KEY"),
    verbose=True,
)

model_with_structured_output = llm.with_structured_output(ToolResponse)
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

    if response.events and response.events[0].eventId:
        return {
            "events": response.events,
            "tickets": [],
            "message": "Here are the events I found:",
        }
    elif response.tickets and response.tickets[0].ticketId:
        return {
            "events": [],
            "tickets": response.tickets,
            "message": "Here are your tickets:",
        }
    else:
        return {
            "events": [],
            "tickets": [],
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


def ask_agent(messages, user_address):
    config = {"configurable": {"user_address": user_address}}

    response = graph.invoke(
        config=config,
        input={
            "messages": [
                (
                    "system",
                    """You are Tikeetron Bot. Follow these rules:
1. For event-related questions (e.g., "What events are happening?"), call `get_events` and pass any available event context (such as location, date, or category) into the arguments. Retrieve the eventId, name, and category, and return the event name along with a brief description of the event.
2. For ticket/transaction inquiries, call `get_my_tickets`. Retrieve the ticketId, type, eventName, eventStartDate, and eventEndDate, and return the event name along with a brief description of the event.
3. For general queries (NFTs or Tikeetron info), call `get_to_know_tikeetron`.

Present the event data clearly in your response, without asking for clarification unless absolutely necessary. Ensure all responses are based on the provided data, and do not introduce any fabricated information.

Provide all responses in Markdown format.
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
            "events": get_events_by_ids(
                [event.eventId for event in response["events"]]
            ),
            "tickets": get_tickets_by_ids(
                [ticket.ticketId for ticket in response["tickets"]],
                user_address,
            ),
        }
    else:
        return {
            "message": "I'm sorry, I don't have an answer for that.",
        }
