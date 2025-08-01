# app.py
import streamlit as st
from dotenv import load_dotenv
from src.agent.core import create_agent_executor

load_dotenv()

st.set_page_config(page_title="Agentic Offer Letter Generator", page_icon="✍️")
st.title("✍️ Agentic Offer Letter Generator")
st.info("Enter the full name of an employee to generate their offer letter.")

if "agent_executor" not in st.session_state:
    st.session_state.agent_executor = create_agent_executor()

employee_name = st.text_input("Employee Name", placeholder="e.g., Julie Rodriguez")

if st.button("Generate Offer Letter"):
    if employee_name:
        with st.spinner("🤖 The agent is thinking... Please wait."):
            try:
                agent_input = f"Fill out the offer letter template for {employee_name}."
                response = st.session_state.agent_executor.invoke({"input": agent_input})
                st.markdown(response['output'])
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter an employee's name.")