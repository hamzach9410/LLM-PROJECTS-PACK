import streamlit as st

def init_graph_session():
    """Initialize session state for Knowledge Graph RAG."""
    defaults = {
        'neo4j_uri': "bolt://localhost:7687",
        'neo4j_user': "neo4j",
        'graph_ready': False,
        'indexed_docs': [],
        'chat_history': []
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def apply_graph_style():
    """Apply cyber-research UI aesthetics."""
    st.markdown("""
        <style>
        .stMetric { background-color: #f0f2f6; padding: 10px; border-radius: 10px; }
        .reasoning-step { color: #555; font-style: italic; border-left: 2px solid #ccc; padding-left: 10px; }
        </style>
    """, unsafe_content_type=True)
