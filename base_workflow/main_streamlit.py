import streamlit as st
import os
from typing import Any, Union
from langchain_core.runnables import RunnableConfig
from sympy import content
from base_workflow.workflow import workflow_graph

# Output directory
output_dir = 'base_workflow/outputs'
os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists

def process_query(user_input):
    """Process user input and stream results."""
    output_text = ""
    for update in workflow_graph.stream({"messages": [("user", user_input)]}):
        for node_id, value in update.items():
            if isinstance(value, dict) and value.get('messages', []):
                last_message = value['messages'][-1]                
                # If it's the writing agent, save the output
                if node_id == 'writing_agent':
                    st.write(f'{last_message.content}')
                    output_text = last_message.content
                    output_path = f'{output_dir}/writing_agent_output.txt'
                    
                    if os.path.exists(output_path): 
                        os.remove(output_path)
                    
                    with open(output_path, 'w') as f:
                        f.write(output_text)
    
    return output_text


# Streamlit UI
st.title("AI Content Creator")
st.write("Enter a query to explore AI-generated content in real-time!!!")

# User input
user_input = st.text_input("Enter here:", "Tell me about SJ MOSFETs")

if st.button("Start generating report"):
    with st.spinner("Processing..."):
        process_query(user_input)
    st.success("Completed!")

