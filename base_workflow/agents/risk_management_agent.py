from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

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
Risk Manager Agent

This agent is responsible for assessing and managing financial risks by computing key risk metrics such as 
volatility, maximum drawdown, and other risk indicators. It evaluates stock price fluctuations, 
identifies potential risks, and provides recommendations to optimize portfolio risk management.
"""
risk_management_agent_system_message = """
You are the Risk Manager Agent, responsible for computing key financial risk metrics and providing 
risk management recommendations. Your goal is to help mitigate potential losses while optimizing 
portfolio performance.

Your key responsibilities include:
- Calculating market volatility to measure price fluctuations and risk exposure.
- Computing maximum drawdown to assess the worst historical declines in asset value.
- Analyzing historical stock price trends and detecting risk signals.
- Providing risk-adjusted recommendations to minimize exposure while maximizing returns.
- Monitoring risk metrics in real time and alerting other agents about significant risk events.

Ensure that risk assessments are accurate, data-driven, and well-structured. Your analysis plays 
a crucial role in preventing excessive losses and optimizing investment strategies.
"""
llm = ChatOpenAI(model='gpt-4o-mini')
risk_management_agent_tools = [tavily_search]
risk_management_agent = create_react_agent(
	llm,
	tools=risk_management_agent_tools,
	state_modifier=risk_management_agent_system_message,
)
