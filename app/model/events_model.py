from pydantic import BaseModel


class EventModel(BaseModel):
    id: int
    name: str
    location: str


class EventsModel(BaseModel):
    events: list[EventModel]
