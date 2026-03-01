import streamlit as st

def initialize_session():
    """Initialize session state for URLs and tracking."""
    if 'urls' not in st.session_state:
        st.session_state.urls = []
    if 'urls_loaded' not in st.session_state:
        st.session_state.urls_loaded = set()

def apply_custom_style():
    """Apply premium aesthetics to the Streamlit app."""
    st.markdown("""
        <style>
        .main {
            background-color: #f8f9fa;
        }
        .stButton>button {
            border-radius: 8px;
            font-weight: 600;
        }
        .stTextInput>div>div>input {
            border-radius: 8px;
        }
        </style>
    """, unsafe_content_type=True)
