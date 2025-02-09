from langgraph.graph import StateGraph, MessagesState, START
from langchain_openai import ChatOpenAI
# from base_workflow.utils.make_supervisor_node import make_supervisor_node

from base_workflow.nodes import data_agent_node, writing_agent_node


workflow = StateGraph(MessagesState)

workflow.add_node("data_agent", data_agent_node)
workflow.add_node("writing_agent", writing_agent_node)
workflow.add_edge(START, "data_agent")

workflow_graph = workflow.compile()

def main():
	user_input = 'Summarize recent trends in semiconductor fabrication'
	for s in workflow_graph.stream({"messages": [("user", user_input)]}):
		print(s)
		print("----")


if __name__ == '__main__':
	main()