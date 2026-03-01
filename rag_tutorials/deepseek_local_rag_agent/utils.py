import streamlit as st
import re

def init_deepseek_session():
    """Initialize session state for DeepSeek RAG."""
    session_defaults = {
        'qdrant_api_key': "",
        'qdrant_url': "",
        'exa_api_key': "",
        'model_version': "deepseek-r1:1.5b",
        'history': [],
        'processed_sources': [],
        'rag_enabled': True,
        'use_web_search': False,
        'force_web_search': False,
        'similarity_threshold': 0.7
    }
    for key, val in session_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

def parse_deepseek_response(text):
    """DeepSeek often includes <think> blocks; parse them for transparency."""
    think_pattern = r'<think>(.*?)</think>'
    think_match = re.search(think_pattern, text, re.DOTALL)
    
    if think_match:
        thinking = think_match.group(1).strip()
        final_answer = re.sub(think_pattern, '', text, flags=re.DOTALL).strip()
        return thinking, final_answer
    return None, text

def apply_deepseek_style():
    """Premium UI styling for local AI lab."""
    st.markdown("""
        <style>
        .thinking-container {
            background-color: #f8f9fa;
            border-left: 4px solid #007bff;
            padding: 10px;
            font-family: monospace;
            font-size: 0.9em;
            margin-bottom: 10px;
        }
        .stChatFloatingInputContainer { background-color: transparent; }
        </style>
    """, unsafe_content_type=True)
