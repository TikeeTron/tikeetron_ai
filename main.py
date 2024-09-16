from fastapi import FastAPI
from app.chatbot.chain import ask_agent
from app.dto.ask_param import AskParam

app = FastAPI()


@app.post("/ask")
async def ask(param: AskParam) -> str:
    return ask_agent(param.question)
