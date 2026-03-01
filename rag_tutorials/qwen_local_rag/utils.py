import streamlit as st

def init_qwen_session():
    """Initialize session state for Qwen RAG."""
    defaults = {
        'model_version': "qwen2.5:1.5b",
        'history': [],
        'processed_docs': [],
        'vector_store': None,
        'exa_key': "",
        'use_web': False
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def apply_qwen_style():
    """Apply high-end research lab aesthetics."""
    st.markdown("""
        <style>
        .stApp { background-color: #0d1117; color: #c9d1d9; }
        .stChatMessage { border: 1px solid #30363d; border-radius: 10px; }
        .stSidebar { background-color: #161b22; }
        </style>
    """, unsafe_content_type=True)

def show_model_info():
    st.info("**Qwen 2.5:** High-performance local reasoning model optimized for strategic data processing.")
    st.info("**Gemma 3:** Multimodal-ready local intelligence with extended context capabilities.")
