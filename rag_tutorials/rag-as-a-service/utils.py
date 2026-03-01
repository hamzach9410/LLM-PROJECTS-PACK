import streamlit as st

def init_raas_session():
    """Initialize session state for RAG-as-a-Service (RaaS)."""
    defaults = {
        'engine': None,
        'ragie_key': "",
        'anthropic_key': "",
        'indexed': False,
        'chat_history': []
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def apply_raas_style():
    """Apply high-tech industrial UI aesthetics."""
    st.markdown("""
        <style>
        .stApp { background-color: #f4f7f6; }
        .stAlert { border-radius: 10px; }
        .stButton>button { width: 100%; border-radius: 5px; background-color: #2c3e50; color: white; }
        </style>
    """, unsafe_content_type=True)
