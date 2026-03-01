import streamlit as st

def init_cohere_session():
    """Initialize session state for Cohere RAG."""
    defaults = {
        'cohere_key': "",
        'qdrant_url': "",
        'qdrant_key': "",
        'vs': None,
        'chat_history': [],
        'ready': False
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def apply_cohere_style():
    """Apply professional, focused UI aesthetics."""
    st.markdown("""
        <style>
        .stApp { background-color: #fdfdfd; }
        .stChatMessage { padding: 1rem; border-radius: 8px; }
        </style>
    """, unsafe_content_type=True)
