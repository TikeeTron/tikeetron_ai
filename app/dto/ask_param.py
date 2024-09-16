from pydantic import BaseModel


class AskParam(BaseModel):
    question: str
