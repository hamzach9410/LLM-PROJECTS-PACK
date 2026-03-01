import streamlit as st

def init_blog_session():
    """Initialize session state for AI Blog Search."""
    defaults = {
        'gemini_key': "",
        'qdrant_host': "",
        'qdrant_key': "",
        'vs': None,
        'ready': False
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def apply_blog_style():
    """Apply modern research lab aesthetics."""
    st.markdown("""
        <style>
        .stApp { background-color: #f7f9fc; }
        .stHeader { color: #2c3e50; }
        .stButton>button { border-radius: 8px; font-weight: 600; }
        </style>
    """, unsafe_content_type=True)
