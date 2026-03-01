import streamlit as st

def init_pharma_session():
    """Initialize session state for PharmaQuery."""
    defaults = {
        'gemini_key': "",
        'ready': False,
        'history': []
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def apply_pharma_style():
    """Apply clinical medical research UI aesthetics."""
    st.markdown("""
        <style>
        .stApp { background-color: #f0f4f8; }
        .stHeader { color: #1a365d; }
        .stButton>button { border-radius: 20px; background-color: #2b6cb0; color: white; }
        </style>
    """, unsafe_content_type=True)
