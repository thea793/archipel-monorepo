# Helper function to create a node for a given agent
from turtle import update
from base_workflow.agents import data_agent
from langchain_core.messages import HumanMessage
from langgraph.types import Send, Command
from langgraph.graph import MessagesState
from typing import Literal


def data_agent_node(state: MessagesState) -> Command[Literal['writing_agent']]:
	result = data_agent.invoke(state)
	# print(f"DEBUG: Result from financial_analyst_agent -> {result.content}")

	return Command(
		update={
			'messages': [
				HumanMessage(content=result["messages"][-1].content, name='search')
			]
		},
		# We want our workers to ALWAYS "report back" to the supervisor when done
		goto= 'writing_agent'
		)

