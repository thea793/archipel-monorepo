from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from base_workflow.tools import scrape_webpages


llm = ChatOpenAI(model="gpt-4o")
web_scraper_agent = create_react_agent(llm, tools=[scrape_webpages])