import streamlit as st
import os

def initialize_reasoning_session():
    """Initialize session state for reasoning and sources."""
    if 'knowledge_urls' not in st.session_state:
        st.session_state.knowledge_urls = ["https://www.theunwindai.com/p/mcp-vs-a2a-complementing-or-supplementing"]
    if 'urls_loaded' not in st.session_state:
        st.session_state.urls_loaded = set()
    if 'query' not in st.session_state:
        st.session_state.query = "What is the difference between MCP and A2A protocols?"

def apply_styling():
    """Apply premium aesthetic styling."""
    st.markdown("""
        <style>
        .reasoning-box {
            background-color: #f0f2f6;
            padding: 15px;
            border-radius: 10px;
            border-left: 5px solid #ff4b4b;
        }
        .stTextArea>div>div>textarea {
            border-radius: 10px;
        }
        </style>
    """, unsafe_content_type=True)
