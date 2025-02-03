from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from base_workflow.tools import read_document, python_repl_tool

llm = ChatOpenAI(model="gpt-4o")

chart_generating_agent = create_react_agent(
    llm, tools=[read_document, python_repl_tool]
)