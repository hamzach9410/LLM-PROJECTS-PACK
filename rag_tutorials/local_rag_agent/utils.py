import streamlit as st

def init_local_agent_session():
    """Initialize session state for local agent operations."""
    defaults = {
        'model_id': "llama3.2",
        'docs_indexed': False,
        'chat_history': []
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def apply_local_agent_style():
    """Apply clean, minimal UI aesthetics for local work."""
    st.markdown("""
        <style>
        .stApp { background-color: #f8f9fa; }
        .stChatMessage { border-radius: 15px; }
        </style>
    """, unsafe_content_type=True)
