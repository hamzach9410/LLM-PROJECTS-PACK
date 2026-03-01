import streamlit as st
import anthropic

def init_hybrid_session():
    """Initialize session state for hybrid RAG."""
    vars = {
        'chat_history': [],
        'documents_ready': False,
        'rag_config': None,
        'openai_key': "",
        'anthropic_key': "",
        'cohere_key': "",
        'db_url': "sqlite:///raglite.sqlite"
    }
    for var, val in vars.items():
        if var not in st.session_state:
            st.session_state[var] = val

def run_fallback_query(query, anthropic_key):
    """Fallback to direct LLM if no documents are relevant."""
    try:
        client = anthropic.Anthropic(api_key=anthropic_key)
        resp = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1024,
            messages=[{"role": "user", "content": query}]
        )
        return resp.content[0].text
    except Exception as e:
        return f"Intelligence fallback failed: {str(e)}"

def apply_premium_style():
    """Apply professional UI aesthetics."""
    st.markdown("""
        <style>
        .stActionButton { border-radius: 20px; }
        .stSidebar { background-color: #f0f4f8; }
        </style>
    """, unsafe_content_type=True)
