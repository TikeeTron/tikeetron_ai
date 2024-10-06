import os
import requests

from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig

from dotenv import load_dotenv

load_dotenv()

BASE_API_URL = os.getenv("BASE_API_URL")

session = requests.Session()
session.auth = (os.getenv("HTTP_BASIC_USER"), os.getenv("HTTP_BASIC_PASSWORD"))


def get_tickets_by_ids(
    ticket_ids: list,
    user_address: str,
):
    """use this tool to get the tickets by the ticket ids"""
    if ticket_ids is None or len(ticket_ids) == 0:
        return []

    request_session = session.get(
        f"{BASE_API_URL}/v1/tickets",
        params={
            "ticketIds[]": ticket_ids,
            "buyerAddress": user_address,
        },
    )
    tickets = request_session.json()["data"]

    return tickets


@tool
def get_my_tickets_tool(
    config: RunnableConfig,
):
    """use this tool to get the tickets that the user has, only call this tool if the user asks for their tickets"""
    user_address = config.get("configurable", {}).get("user_address")

    request_session = session.get(
        f"{BASE_API_URL}/v1/tickets",
        params={
            "buyerAddress": user_address,
            "limit": 5,
        },
    )

    response = request_session.json()["data"]

    formatted_response = []
    for ticket in response:
        formatted_response.append(
            {
                "ticketId": ticket["ticketId"],
                "type": ticket["type"],
                "eventName": ticket["event"]["name"],
                "eventStartDate": ticket["event"]["startDate"],
                "eventEndDate": ticket["event"]["endDate"],
            }
        )

    return formatted_response
