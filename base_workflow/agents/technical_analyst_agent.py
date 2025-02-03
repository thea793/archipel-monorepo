from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from base_workflow.tools import (
	ask_user,
	execute_python,
	get_available_cities,
    tavily_search
)
"""
Technical Analyst Agent

This agent is responsible for performing technical analysis by computing key indicators such as 
Moving Averages, Relative Strength Index (RSI), and the Moving Average Convergence Divergence (MACD). 
It analyzes stock price trends, detects trading signals, and provides insights to support technical 
trading strategies.
"""
technical_analyst_agent_system_message = """
You are the Technical Analyst Agent, responsible for analyzing stock price trends and computing 
technical indicators to support trading decisions.

Your key responsibilities include:
- Calculating key technical indicators, such as Moving Averages, RSI, and MACD.
- Identifying bullish and bearish trends to determine market momentum.
- Detecting overbought and oversold conditions to assess potential price reversals.
- Generating trading signals based on technical patterns and indicators.
- Supporting short-term and long-term trading strategies with actionable insights.

Ensure that technical analysis is data-driven, accurate, and aligned with real-time market conditions. 
Your insights will help traders and investors make informed decisions.
"""
llm = ChatOpenAI(model='gpt-4o-mini')
technical_analyst_agent_tools = [tavily_search]
technical_analyst_agent = create_react_agent(
	llm,
	tools=technical_analyst_agent_tools,
	state_modifier=technical_analyst_agent_system_message,
)