from turtle import update
from base_workflow.agents import technical_analyst_agent
from langchain_core.messages import HumanMessage
from langgraph.types import Send, Command
from langgraph.graph import MessagesState
from typing import Literal



def technical_analyst_agent_node(state: MessagesState) -> Command[Literal['supervisor']]:
	result = technical_analyst_agent.invoke(state)
	return Command(
		update={
			'messages': [
				HumanMessage(content=result.content, name='search')
			]
		},
		# We want our workers to ALWAYS "report back" to the supervisor when done
		goto='supervisor'
		)