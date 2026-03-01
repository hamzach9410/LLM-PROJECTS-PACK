import streamlit as st

def init_gemini_session():
    """Initialize session state for Gemini RAG."""
    defaults = {
        'google_api_key': "",
        'qdrant_api_key': "",
        'qdrant_url': "",
        'exa_api_key': "",
        'history': [],
        'processed_sources': [],
        'use_web_search': False,
        'force_web_search': False,
        'similarity_threshold': 0.7
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

def apply_gemini_style():
    """Apply modern Gemini-themed styling."""
    st.markdown("""
        <style>
        .stChatMessage { border-radius: 15px; border: 1px solid #e1e4e8; }
        .stSidebar { background-color: #f8f9ff; }
        </style>
    """, unsafe_content_type=True)
