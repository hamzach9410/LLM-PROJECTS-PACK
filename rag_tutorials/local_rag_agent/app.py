import streamlit as st
import os
from agents_config import get_local_agent
from rag_engine import LocalAgentEngine
from utils import init_local_agent_session, apply_local_agent_style

st.set_page_config(page_title="Local Privacy Hub", layout="wide")
apply_local_agent_style()
init_local_agent_session()

st.title("🛡️ Local Privacy Intelligence Hub")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Local Core")
    model_id = st.text_input("Ollama Model ID", value=st.session_state.model_id)
    st.session_state.model_id = model_id
    
    st.divider()
    st.header("📥 Data Ingestion")
    source_url = st.text_input("Source URL (PDF)", value="https://phi-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf")
    if st.button("🚀 Index to Vault", use_container_width=True):
        with st.spinner("Indexing locally..."):
            agent, kb = get_local_agent(model_id)
            engine = LocalAgentEngine(agent, kb)
            success, msg = engine.ingest_document(url=source_url)
            if success:
                st.success(msg)
                st.session_state.docs_indexed = True

# Main Execution
if not st.session_state.docs_indexed:
    st.info("👋 Welcome! Please index a knowledge source in the sidebar to activate the local intelligence Hub.")
    st.stop()

# Initialize Engine
agent, kb = get_local_agent(st.session_state.model_id)
engine = LocalAgentEngine(agent, kb)

# Q&A Logic
st.divider()
query = st.chat_input("Ask your private agent anything...")
if query:
    with st.chat_message("user"): st.markdown(query)
    with st.chat_message("assistant"):
        resp_box = st.empty()
        full_val = ""
        with st.spinner("Consulting local knowledge..."):
            stream = engine.query_stream(query)
            for chunk in stream:
                if hasattr(chunk, 'content') and chunk.content:
                    full_val += str(chunk.content)
                    resp_box.markdown(full_val + "▌")
            resp_box.markdown(full_val)
            st.session_state.chat_history.append((query, full_val))
