import os
from langchain import hub
from dotenv import load_dotenv
from langchain.agents import create_react_agent, AgentExecutor
from langchain_groq import ChatGroq

from tools.get_tikeetron import GetTikeetronTool, get_tikeetron_tool
from tools.get_my_tickets import GetMyTicketsTool
from tools.get_current_events import GetCurrentEventsTool

load_dotenv()

tools = [
    GetCurrentEventsTool(),
    GetMyTicketsTool(),
    get_tikeetron_tool,
]

llm = ChatGroq(
    model="llama3-70b-8192",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=os.getenv("GROQ_API_KEY"),
    verbose=True,
)

agent = create_react_agent(
    tools=tools,
    llm=llm,
    prompt=hub.pull("hwchase17/react"),
)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

agent_executor.invoke({"input": "what is tikeetron?"})
