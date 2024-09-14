from typing import Optional, Type

from langchain.pydantic_v1 import BaseModel
from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from pydantic import Field


class GetMyTicketsInput(BaseModel):
    user_id: str = Field(description="The user ID to get tickets for")


# @tool("get-my-tickets-tool", args_schema=GetMyTicketsInput, return_direct=True)
# def get_my_tickets(input: GetMyTicketsInput):
#     """Get the tickets that the user has"""
#     return {
#         "tickets": [
#             {
#                 "title": "Ticket 1",
#                 "description": "This is the first ticket",
#                 "date": "2021-01-01"
#             }
#         ]
#     }


class GetMyTicketsTool(BaseTool):
    name: str = "Get My Tickets"
    description: str = "use this tool to get the tickets that the user has"
    args_schema: Type[BaseModel] = GetMyTicketsInput
    return_direct: bool = True

    def _run(
        self,
        input: GetMyTicketsInput,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ):
        """Use the tool."""
        print(input)
        return {
            "events": [
                {
                    "title": "Event 1",
                    "description": "This is the first event",
                    "date": "2021-01-01",
                },
            ]
        }

    def _arun(
        self,
        input: GetMyTicketsInput,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ):
        """Use the tool asynchronously."""
        return self._run(input, run_manager=run_manager.get_sync())
