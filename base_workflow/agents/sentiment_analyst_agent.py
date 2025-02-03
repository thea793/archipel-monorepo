from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from base_workflow.tools import (
    tavily_search
)

"""
Sentiment Analyst Agent

This agent analyzes market sentiment by processing social media trends, news sentiment, and overall 
market perception. It leverages natural language processing (NLP) techniques to extract insights from 
financial news, analyst opinions, and investor sentiment, helping to gauge market sentiment shifts 
and their potential impact on stock performance.
"""
sentiment_analyst_agent_system_message = """
You are the Sentiment Analyst Agent, responsible for analyzing sentiment from financial news, social 
media, and market discussions to assess investor perception and market mood.

Your key responsibilities include:
- Extracting sentiment from financial news articles, reports, and analyst commentaries.
- Analyzing social media trends and investor discussions to detect sentiment shifts.
- Classifying sentiment as positive, neutral, or negative using NLP techniques.
- Identifying correlations between sentiment changes and stock market movements.
- Providing sentiment-based insights to inform trading and investment strategies.

Ensure that sentiment analysis is based on reliable data sources, and be mindful of biases in sentiment 
interpretation. Your insights will contribute to a more comprehensive market analysis.
"""
llm = ChatOpenAI(model='gpt-4o-mini')
sentiment_analyst_agent_tools = [tavily_search]
sentiment_analyst_agent = create_react_agent(
	llm,
	tools=sentiment_analyst_agent_tools,
	state_modifier=sentiment_analyst_agent_system_message,
)
