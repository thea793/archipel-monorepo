from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.types import Send, Command
from langgraph.graph import MessagesState
from typing import Literal
from base_workflow.utils import create_agent

from base_workflow.tools import (
	ask_user,
	execute_python,
	get_available_cities,
	get_restaurants_and_menu_in_city,
	order_pizza,
    tavily_search
)
from base_workflow.utils import create_agent

"""
Financial Analyst Agent

This agent is responsible for analyzing financial statements and evaluating key valuation metrics 
such as Price-to-Earnings (P/E), Price-to-Book (P/B), and Return on Equity (ROE). It extracts 
relevant financial data, performs fundamental analysis, and provides insights into a company's 
financial health and valuation.
"""
financial_analyst_agent_system_message = """
You are the Financial Analyst Agent, responsible for evaluating financial statements and key 
valuation metrics to assess a company's financial health and investment potential.

Your key responsibilities include:
- Extracting financial data from income statements, balance sheets, and cash flow statements.
- Calculating valuation metrics such as Price-to-Earnings (P/E), Price-to-Book (P/B), and Return on Equity (ROE).
- Comparing financial ratios against industry benchmarks and historical data.
- Identifying trends, strengths, and risks in a company's financial performance.
- Providing clear, data-driven insights to support investment decision-making.

Ensure accuracy in financial calculations, handle missing data appropriately, and communicate insights 
in a structured, easy-to-understand manner. Your analysis plays a crucial role in stock recommendations 
and portfolio management.
"""
llm = ChatOpenAI(model='gpt-4o-mini')
financial_analyst_agent_tools = [tavily_search]
financial_analyst_agent = create_agent(
	llm,
	tools=financial_analyst_agent_tools,
	system_message=financial_analyst_agent_system_message,
)

def financial_analyst_agent_node(state: MessagesState) -> Command[Literal['supervisor']]:
	print(f"DEBUG: Received state -> {state}")
	result = financial_analyst_agent.invoke(state)
	print(f"DEBUG: Result from financial_analyst_agent -> {result.content}")
	return Command(
		update={
			'messages': [
				HumanMessage(content=result.content, name='search')
			]
		},
		# We want our workers to ALWAYS "report back" to the supervisor when done
		goto='supervisor'
		)

test_input = {"messages": [("user", "Analyze Tesla's financial health and valuation metrics.")]}
response = financial_analyst_agent.invoke(test_input)
print(f"Agent Response: {response}")
