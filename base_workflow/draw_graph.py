from base_workflow.workflow import super_graph
from base_workflow.utils.stock_graph import research_graph
from base_workflow.utils.writing_team_graph import paper_writing_graph
from langchain_core.runnables.graph import MermaidDrawMethod


def main():
	with open('graph.png', 'wb') as fp:
		fp.write(
			paper_writing_graph.get_graph().draw_mermaid_png(
				draw_method=MermaidDrawMethod.API,
			)
		)


if __name__ == '__main__':
	main()
