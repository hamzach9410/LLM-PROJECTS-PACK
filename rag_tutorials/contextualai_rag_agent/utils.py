import streamlit as st
import re

def init_contextual_session():
    """Initialize session state for Contextual AI."""
    session_vars = {
        "api_key_submitted": False,
        "contextual_api_key": "",
        "base_url": "https://api.contextual.ai/v1",
        "agent_id": "",
        "datastore_id": "",
        "chat_history": [],
        "last_raw_response": None,
        "last_user_query": ""
    }
    for var, val in session_vars.items():
        if var not in st.session_state:
            st.session_state[var] = val

def post_process_answer(text: str) -> str:
    """Clean up agent response formatting."""
    text = re.sub(r"\(\s*\)", "", text)
    text = text.replace("• ", "\n- ")
    return text.strip()

def apply_contextual_style():
    """Apply premium aesthetics."""
    st.markdown("""
        <style>
        .stChatMessage { border-radius: 12px; margin-bottom: 10px; }
        .stSidebar { background-color: #f1f3f6; }
        </style>
    """, unsafe_content_type=True)
