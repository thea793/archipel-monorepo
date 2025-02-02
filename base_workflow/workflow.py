from langgraph.graph import StateGraph, MessagesState, START
from langchain_openai import ChatOpenAI
# from base_workflow.utils.make_supervisor_node import make_supervisor_node

from base_workflow.nodes import (
	financial_analyst_agent_node, 
	real_time_data_agent_node, 
	reporter_agent_node, 
	risk_management_agent_node, 
	sentiment_analyst_agent_node, 
	technical_analyst_agent_node
	)



# Initialize the Language Model
llm = ChatOpenAI(model='gpt-4o-mini')

# # Make a Supervisor Node
# supervisor_node = make_supervisor_node(
# 	llm,
# 	[
# 		'financial_analyst_agent',
# 		'real_time_data_agent',
# 		'risk_management_agent',
# 		'sentiment_analyst_agent',
# 		'technical_analyst_agent',
# 	],
# )
#############################################################################################################
### from now on supervisor node
from typing import Literal
from typing_extensions import TypedDict

from langgraph.graph import MessagesState, END
from langgraph.types import Command


members = ['financial_analyst_agent',
		'real_time_data_agent',
		'risk_management_agent',
		'sentiment_analyst_agent',
		'technical_analyst_agent',]
# Our team supervisor is an LLM node. It just picks the next agent to process
# and decides when the work is completed
options = members + ["FINISH"]

system_prompt = (
    "You are a supervisor tasked with managing a conversation between the"
    f" following workers: {members}. Given the following user request,"
    " respond with the worker to act next. Each worker will perform a"
    " task and respond with their results and status. When finished,"
    " respond with FINISH."
)


class Router(TypedDict):
    """Worker to route to next. If no workers needed, route to FINISH."""

    next: Literal['financial_analyst_agent',
		'real_time_data_agent',
		'risk_management_agent',
		'sentiment_analyst_agent',
		'technical_analyst_agent', "FINISH"]


llm = ChatOpenAI(model='gpt-4o-mini')


class State(MessagesState):
    next: str


def supervisor_node(state: State) -> Command[Literal['financial_analyst_agent',
													'real_time_data_agent',
													'risk_management_agent',
													'sentiment_analyst_agent',
													'technical_analyst_agent', "__end__"]]:
    messages = [
        {"role": "system", "content": system_prompt},
    ] + state["messages"]
    response = llm.with_structured_output(Router).invoke(messages)
    goto = response["next"]
    if goto == "FINISH":
        goto = END

    return Command(goto=goto, update={"next": goto})

######end of the supervisor node
################################################################################################################
# Initialize the workflow with the appropriate state
workflow = StateGraph(MessagesState)
# Add the 'supervisor' node
workflow.add_node('supervisor', supervisor_node)

# Define all expert nodes in a dictionary for easy management
expert_nodes = {
	'financial_analyst_agent': financial_analyst_agent_node,
	'real_time_data_agent': real_time_data_agent_node,
	'reporter_agent': reporter_agent_node,
	'risk_management_agent': risk_management_agent_node,
	'sentiment_analyst_agent': sentiment_analyst_agent_node,
	'technical_analyst_agent': technical_analyst_agent_node,
}

# Add all expert nodes to the workflow
for node_name, node in expert_nodes.items():
	workflow.add_node(node_name, node)

# Connect 'START' to 'supervisor'
workflow.add_edge(START, 'supervisor')

# Compile the workflow graph with the updated configuration
workflow_graph = workflow.compile()

################################################################################################################
#main function here
def main():
	print('Running the stock recommendation workflow...')
	user_input = 'Can you recommend a good oil stock?'
	for s in workflow_graph.stream({"messages": [("user", user_input)]}, subgraphs=True):
		print(s)
		print("----")


if __name__ == '__main__':
	main()