import getpass
import os
from typing import Literal
from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.types import Command
from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from base_workflow.nodes import (sentiment_analyst_agent_node, web_scraper_node)


def _set_if_undefined(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"Please provide your {var}")

_set_if_undefined("OPENAI_API_KEY")
_set_if_undefined("TAVILY_API_KEY")

class State(MessagesState):
    next: str


def make_supervisor_node(llm: BaseChatModel, members: list[str]) -> str:
    options = ["FINISH"] + members
    system_prompt = (
        "You are a supervisor tasked with managing a conversation between the"
        f" following workers: {members}. Given the following user request,"
        " respond with the worker to act next. Each worker will perform a"
        " task and respond with their results and status."
        "You must ensure all necessary workers contribute before concluding the process."
        "You must ensure that no worker repeats tasks unnecessarily."
        "When finished, respond with FINISH."
    )

    class Router(TypedDict):
        """Worker to route to next. If no workers needed, route to FINISH."""

        next: Literal[*options]

    def supervisor_node(state: State) -> Command[Literal[*members, "__end__"]]:
        """An LLM-based router."""
        messages = [
            {"role": "system", "content": system_prompt},
        ] + state["messages"]
        response = llm.with_structured_output(Router).invoke(messages)
        goto = response["next"]
        if goto == "FINISH":
            goto = END

        return Command(goto=goto, update={"next": goto})

    return supervisor_node

llm = ChatOpenAI(model="gpt-4o")

research_supervisor_node = make_supervisor_node(llm, ["sentiment_analyst_agent", "web_scraper"])
research_builder = StateGraph(State)
research_builder.add_node("supervisor", research_supervisor_node)
research_builder.add_node("sentiment_analyst_agent", sentiment_analyst_agent_node)
research_builder.add_node("web_scraper", web_scraper_node)
research_builder.add_edge(START, "supervisor")
research_graph = research_builder.compile()

def call_research_team(state: State) -> Command[Literal["supervisor"]]:
    response = research_graph.invoke({"messages": state["messages"][-1]})
    return Command(
        update={
            "messages": [
                HumanMessage(
                    content=response["messages"][-1].content, name="research_team"
                )
            ]
        },
        goto="supervisor",
    )

if __name__ == '__main__':
    for s in research_graph.stream(
        {"messages": [("user", "Can you recommend a good oil stock?")]},
        {"recursion_limit": 10},
    ):
        print(s)
        print("---")