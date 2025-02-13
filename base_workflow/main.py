from typing import Any, Union
from langchain_core.runnables import RunnableConfig
from sympy import content
from base_workflow.workflow import workflow_graph
import os

output_dir = 'base_workflow/outputs'

def main():
	user_input = 'Tell me about SJ MOSFET'
	for update in workflow_graph.stream({"messages": [("user", user_input)]}):
		for node_id, value in update.items():
			if isinstance(value, dict) and value.get('messages', []):
				last_message = value['messages'][-1]
				if node_id == 'writing_agent':
					print (f'{node_id}: {last_message.content}')
					output_path = f'{output_dir}/writing_agent_output.txt'
					if os.path.exists(output_path): 
						os.remove(output_path)
					with open(f'{output_dir}/writing_agent_output.txt', 'w') as f:
						f.write(last_message.content)


if __name__ == '__main__':
	main()