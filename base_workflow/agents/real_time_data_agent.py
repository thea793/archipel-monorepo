from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from base_workflow.tools import (
	ask_user,
	execute_python,
	get_available_cities,
    tavily_search
)
"""
Real-Time Data Agent
This agent connects to stock market APIs to fetch and process real-time market data. 
It continuously retrieves up-to-date stock prices, trading volumes, and other relevant financial metrics, 
enabling real-time analysis and decision-making within the multi-agent stock recommendation system.
"""
real_time_data_agent_system_message = """
You are the Real-Time Data Agent, responsible for retrieving and processing real-time stock market data. 
Your primary role is to connect to stock market APIs, fetch live financial data, and ensure accurate and 
timely updates for downstream analysis. 

Responsibilities:
- Continuously fetch real-time stock prices, trading volumes, and market indicators.
- Handle API rate limits and ensure data retrieval is efficient and reliable.
- Preprocess and format the data for further analysis by other agents.
- Provide up-to-date financial insights to support decision-making.
- Handle errors and missing data gracefully, ensuring robustness.

Maintain accuracy, reliability, and efficiency in data retrieval, as this data is critical for real-time 
stock analysis and recommendations.
"""
llm = ChatOpenAI(model='gpt-4o-mini')
real_time_data_agent_tools = [tavily_search]
real_time_data_agent = create_react_agent(
	llm,
	tools=real_time_data_agent_tools,
	state_modifier=real_time_data_agent_system_message,
)
