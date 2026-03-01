import streamlit as st

def init_gpt5_session():
    """Initialize session state for GPT-5 RAG."""
    defaults = {
        'openai_api_key': "",
        'knowledge_urls': ["https://www.theunwindai.com/p/mcp-vs-a2a-complementing-or-supplementing"],
        'urls_loaded': set(),
        'chat_history': []
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

def apply_gpt5_style():
    """Apply premium dark-themed aesthetics."""
    st.markdown("""
        <style>
        .stApp { background-color: #0d1117; color: #c9d1d9; }
        .stButton>button { border-radius: 8px; font-weight: bold; }
        </style>
    """, unsafe_content_type=True)
