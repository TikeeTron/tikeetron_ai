from typing import Optional, Type
from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from pydantic import Field, BaseModel


class GetCurrentEventsInput(BaseModel):
    category: Optional[str] = Field(
        description="category of events, e.g. sports, music"
    )


class GetCurrentEventsTool(BaseTool):
    name: str = "Get Current Events"
    description: str = "use this tool to get the current events"
    args_schema: Type[GetCurrentEventsInput] = GetCurrentEventsInput
    return_direct: bool = True

    def _run(
        self,
        input: GetCurrentEventsInput,
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
                {
                    "title": "Event 2",
                    "description": "This is the second event",
                    "date": "2021-01-02",
                },
            ]
        }

    async def _arun(
        self,
        input: GetCurrentEventsInput,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ):
        """Use the tool asynchronously."""
        return self._run(input, run_manager=run_manager.get_sync())
