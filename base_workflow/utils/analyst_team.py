import getpass
import os
from typing import Literal, Union
from chromadb.utils.rendezvous_hash import Members
from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.types import Command
from sympy.strategies.rl import subs
from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from base_workflow.nodes import (market_analyst_node, social_media_analyst_node, news_analyst_node, fundamentals_analyst_node)


def _set_if_undefined(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"Please provide your {var}")

_set_if_undefined("OPENAI_API_KEY")
_set_if_undefined("TAVILY_API_KEY")

class State(MessagesState):
    next: str

"""
def make_supervisor_node(llm: BaseChatModel, members: list[str]) -> str:
    options = members + ["FINISH"]
    system_prompt = (
        "You are a supervisor tasked with managing a conversation between the"
        f" following workers: {members}. Given the following user request,"
        " respond with the worker to act next. Each worker will perform a"
        " task and respond with their results and status."
        "Only call each worker once unless absolutely necessary."
        "You must ensure all necessary workers contribute before concluding the process."
        "You must ensure that no worker repeats tasks unnecessarily."
        "When finished, respond with FINISH."
    )

    class Router(TypedDict):
        # Worker to route to next. If no workers needed, route to FINISH.

        next: Literal[*options]

    def supervisor_node(state: State) -> Command[Literal[*members, "__end__"]]:
        #An LLM-based router.
        messages = [
            {"role": "system", "content": system_prompt},
        ] + state["messages"]
        response = llm.with_structured_output(Router).invoke(messages)
        goto = response["next"]
        if goto == "FINISH":
            goto = END

        return Command(goto=goto, update={"next": goto})
    return supervisor_node
"""

llm = ChatOpenAI(model="gpt-4o")
def supervisor_node(state: State) -> Command[Literal["market_analyst", "social_media_analyst", "news_analyst", "fundamentals_analyst", "__end__"]]:
    members = ["market_analyst", "social_media_analyst", "news_analyst", "fundamentals_analyst"]
    system_prompt = (
        "You are a supervisor tasked with managing a conversation between the"
        f" following workers: {members}. "
        "You should let the workers work sequentially."
        " Each worker will perform a task and respond with their results and status."
        "You must ensure all necessary workers contribute before concluding the process."
        "Every worker only work once."
        "When finished, respond with FINISH."
    )

    class Router(TypedDict):
        next: Union[Literal["market_analyst"], Literal["social_media_analyst"], Literal["news_analyst"], Literal["fundamentals_analyst"], Literal["FINISH"]]

    messages = [
            {"role": "system", "content": system_prompt},
        ] + state["messages"]
    response = llm.with_structured_output(Router).invoke(messages)
    goto = response["next"]
    if goto == "FINISH":
        goto = END

    return Command(goto=goto, update={"next": goto})

#research_team_supervisor_node = make_supervisor_node(llm, ["market_analyst", "social_media_analyst", "news_analyst", "fundamentals_analyst"])
research_builder = StateGraph(State)
research_builder.add_node("supervisor", supervisor_node)
research_builder.add_node("market_analyst", market_analyst_node)
research_builder.add_node("social_media_analyst", social_media_analyst_node)
research_builder.add_node("news_analyst", news_analyst_node)
research_builder.add_node("fundamentals_analyst", fundamentals_analyst_node)
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
        {"messages": [("user", "Can you analysis current tendency of Apple Inc.'s stock price?")]},
        #subgraphs=True,
        {"recursion_limit": 10}):
        print(s)
        print("---")