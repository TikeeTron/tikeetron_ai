from typing import Optional, Type

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from pydantic import Field, BaseModel


class GetMyTicketsInput(BaseModel):
    user_id: str = Field(description="The user ID to get tickets for")


class GetMyTicketsTool(BaseTool):
    name: str = "get_my_tickets"
    description: str = "use this tool to get the tickets that the user has, only call this tool if the user asks for their tickets"
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
