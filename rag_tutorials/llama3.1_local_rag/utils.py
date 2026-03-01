import streamlit as st

def init_local_session():
    """Initialize session state for Local RAG."""
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'url_loaded' not in st.session_state:
        st.session_state.url_loaded = False

def apply_local_style():
    """Apply clean, focused UI aesthetics."""
    st.markdown("""
        <style>
        .stTextInput>div>div>input { border-radius: 10px; }
        .success-box { padding: 10px; background-color: #d4edda; border-radius: 5px; }
        </style>
    """, unsafe_content_type=True)
