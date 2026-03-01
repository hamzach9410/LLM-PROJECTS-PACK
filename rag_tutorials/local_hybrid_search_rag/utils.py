import streamlit as st

def init_local_hybrid_session():
    """Initialize session state for local hybrid search."""
    defaults = {
        'llm_path': "",
        'embedder_path': "",
        'db_url': "sqlite:///local_rag.sqlite",
        'rag_config': None,
        'chat_history': [],
        'docs_loaded': False
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def apply_local_hybrid_style():
    """Apply focused technical research UI aesthetics."""
    st.markdown("""
        <style>
        .stChatInput { border-top: 1px solid #ddd; }
        .sidebar .stTextInput { font-size: 0.8em; }
        </style>
    """, unsafe_content_type=True)
