from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from base_workflow.tools import read_document, create_outline

llm = ChatOpenAI(model="gpt-4o")
bearish_researcher_system_message = ""
bearish_researcher_tools = []

bearish_researcher = create_react_agent(
    llm,
    tools=bearish_researcher_tools,
    state_modifier=bearish_researcher_system_message,
)

