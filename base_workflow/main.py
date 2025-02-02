from typing import Any, Union
from langchain_core.runnables import RunnableConfig
# from base_workflow.workflow import workflow_graph
from langgraph.graph import StateGraph, MessagesState, START
from langchain_openai import ChatOpenAI
from sqlalchemy import false
from base_workflow.nodes import (financial_analyst_agent_node)
# def run_graph(input: Union[dict[str, Any], Any], config: RunnableConfig):
# 	"""Run the workflow graph with the given input and configuration."""
# 	# events = workflow_graph.stream(input, config, stream_mode='values')
# 	# for event in events:
# 	# 	if 'messages' in event:
# 	# 		event['messages'][-1].pretty_print()
# 	# 		print('----')
# 	user_input = 'Can you recommend a good oil stock?'
# 	for s in workflow_graph.stream({"messages": [("user", input)]}, subgraphs=True):
# 		print(s)
# 		print("----")
workflow = StateGraph(MessagesState)
# Add the 'supervisor' node
workflow.add_edge(START, 'financial_analyst_agent')
workflow.add_node('financial_analyst_agent', financial_analyst_agent_node)
workflow_graph = workflow.compile()

def main():
	print('Running the stock recommendation workflow...')
	user_input = 'Can you recommend a good oil stock?'
	for s in workflow_graph.stream({"messages": [("user", user_input)]}, subgraphs=True):
		print(s)
		print("----")


if __name__ == '__main__':
	main()
