from base_workflow.agents import web_scraper_agent
from langchain_core.messages import HumanMessage
from langgraph.types import Command
from langgraph.graph import MessagesState
from typing import Literal

class State(MessagesState):
    next: str

def web_scraper_node(state: State) -> Command[Literal["supervisor"]]:
    result = web_scraper_agent.invoke(state)
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="web_scraper")
            ]
        },
        # We want our workers to ALWAYS "report back" to the supervisor when done
        goto="supervisor",
    )