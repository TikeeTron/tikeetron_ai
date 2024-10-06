from typing import Annotated
from fastapi import FastAPI, Header
from app.chatbot.chain import ask_agent
from app.dto.ask_param import AskParam

app = FastAPI()


@app.post("/ask")
async def ask(
    param: AskParam,
    user_address: Annotated[str | None, Header()] = None,
):
    return ask_agent(param.question, user_address)
