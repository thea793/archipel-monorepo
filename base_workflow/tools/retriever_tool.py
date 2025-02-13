from bs4.filter import SoupStrainer
import os
from langchain import hub
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.tools.retriever import create_retriever_tool
from langchain_community.document_loaders import PyPDFLoader



current_dir = os.path.dirname(__file__)

file_path = os.path.join(
	current_dir,
	'..',
	'data/Infineon-ProductBrochure_CoolMOS_Benefits_in_Hard_Soft_Switching-ProductBrochure-v07_01-EN.pdf',
)

loader = PyPDFLoader(file_path)
pages = loader.load_and_split()
data_vectorstore = Chroma.from_documents(
	documents=pages,
	collection_name='rag-chroma',
	embedding=OpenAIEmbeddings(),
)
retriever = data_vectorstore.as_retriever()

retriever_tool = create_retriever_tool(
    retriever,
    "search_agents_answer",
    "Searches and returns context from LLM Powered Autonomous Agents. Answering questions about the agents.",
)
