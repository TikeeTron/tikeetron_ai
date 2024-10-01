from typing import Optional
from pydantic import BaseModel
from langgraph.graph import MessagesState


class EventResponse(BaseModel):
    """Model for response of event"""

    id: str
    name: str
    category: str


class EventsResponse(BaseModel):
    """Model for response of events"""

    events: list[EventResponse]


class AgentState(MessagesState):
    events: list[EventResponse]
