from typing import Optional
from pydantic import BaseModel
from langgraph.graph import MessagesState


class TicketResponse(BaseModel):
    """Model for response of ticket"""

    ticketId: int
    type: str
    eventName: str
    eventStartDate: str
    eventEndDate: str


class EventResponse(BaseModel):
    """Model for response of event"""

    eventId: str
    name: str
    category: str


class ToolResponse(BaseModel):
    """Model for response of events"""

    events: list[EventResponse]
    tickets: list[TicketResponse]


class AgentState(MessagesState):
    events: list[EventResponse]
    tickets: list[TicketResponse]
