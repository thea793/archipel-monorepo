from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from base_workflow.tools import read_document, create_outline

llm = ChatOpenAI(model="gpt-4o")

note_taking_agent = create_react_agent(
    llm,
    tools=[create_outline, read_document],
    state_modifier=(
        "You can read documents and create outlines for the document writer. "
        "Don't ask follow-up questions."
    ),
)

