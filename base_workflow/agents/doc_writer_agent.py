from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from base_workflow.tools import write_document, edit_document, read_document

llm = ChatOpenAI(model="gpt-4o")

doc_writer_agent = create_react_agent(
    llm,
    tools=[write_document, edit_document, read_document],
    state_modifier=(
        "You can read, write and edit documents based on note-taker's outlines. "
        "Don't ask follow-up questions."
    ),
)
