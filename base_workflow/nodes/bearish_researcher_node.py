from turtle import update
from base_workflow.agents import bearish_researcher
from langchain_core.messages import HumanMessage
from langgraph.types import Send, Command
from langgraph.graph import MessagesState
from typing import Literal


def bearish_researcher_node(state: MessagesState) -> Command[Literal['supervisor']]:
	result = bearish_researcher.invoke(state)
	return Command(
		update={
			'messages': [
				HumanMessage(content=result["messages"][-1].content, name='search')
			]
		},
		# We want our workers to ALWAYS "report back" to the supervisor when done
		goto='supervisor'
		)
