from typing_extensions import TypedDict
from typing import Literal
from langgraph.graph import MessagesState, StateGraph, START, END
from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.types import Command
from langchain_openai import ChatOpenAI
from base_workflow.utils.stock_graph import call_research_team
from base_workflow.utils.writing_team_graph import call_paper_writing_team

class State(MessagesState):
    next: str
    
llm = ChatOpenAI(model="gpt-4o")
def make_supervisor_node(llm: BaseChatModel, members: list[str]) -> str:
    options = ["FINISH"] + members
    system_prompt = (
        "You are a supervisor tasked with managing a conversation between the"
        f" following workers: {members}. Given the following user request,"
        " respond with the worker to act next. Each worker will perform a"
        " task and respond with their results and status. When finished,"
        " respond with FINISH."
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

teams_supervisor_node = make_supervisor_node(llm, ["research_team", "writing_team"])

# Define the graph.
super_builder = StateGraph(State)
super_builder.add_node("supervisor", teams_supervisor_node)
super_builder.add_node("research_team", call_research_team)
super_builder.add_node("writing_team", call_paper_writing_team)

super_builder.add_edge(START, "supervisor")
super_graph = super_builder.compile()

if __name__ == "__main__":
	for s in super_graph.stream(
		{
			"messages": [
				("user", "Can you recommend a good oil stock?")
			],
		},
		{"recursion_limit": 150},
	):
		print(s)
		print("---")