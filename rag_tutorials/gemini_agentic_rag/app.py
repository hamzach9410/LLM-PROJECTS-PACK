import streamlit as st
import os
from agents_config import get_gemini_agents
from vector_store import VectorManager
from rag_engine import GeminiRAGEngine
from utils import init_gemini_session, apply_gemini_style

# Page configuration
st.set_page_config(
    page_title="Gemini Agentic Lab",
    page_icon="🤔",
    layout="wide"
)

apply_gemini_style()
init_gemini_session()

st.title("🤔 Gemini Agentic RAG Lab")
st.markdown("---")

# Sidebar - Configuration
with st.sidebar:
    st.header("🔑 Authentication")
    g_key = st.text_input("Google API Key", type="password", value=st.session_state.google_api_key)
    q_url = st.text_input("Qdrant URL", value=st.session_state.qdrant_url)
    q_key = st.text_input("Qdrant API Key", type="password", value=st.session_state.qdrant_api_key)
    
    st.session_state.google_api_key = g_key
    st.session_state.qdrant_url = q_url
    st.session_state.qdrant_api_key = q_key
    
    st.divider()
    st.header("🌐 Web Intelligence")
    st.session_state.use_web_search = st.checkbox("Enable Exa Search Fallback", value=st.session_state.use_web_search)
    if st.session_state.use_web_search:
        st.session_state.exa_api_key = st.text_input("Exa API Key", type="password", value=st.session_state.exa_api_key)

    if st.button("🗑️ Reset Intelligence History", use_container_width=True):
        st.session_state.history = []
        st.rerun()

# Main Logic
if not all([st.session_state.google_api_key, st.session_state.qdrant_url, st.session_state.qdrant_api_key]):
    st.info("👋 Welcome! Please configure your Google and Qdrant credentials in the sidebar to activate the lab.")
    st.stop()

# Initialize Backend
v_manager = VectorManager(st.session_state.qdrant_url, st.session_state.qdrant_api_key, st.session_state.google_api_key)
v_manager.setup_collection()
vstore = v_manager.get_vectorstore()

rewriter, web_agent, rag_agent = get_gemini_agents(
    st.session_state.google_api_key,
    st.session_state.exa_api_key if st.session_state.use_web_search else None
)
engine = GeminiRAGEngine(vstore, rewriter, rag_agent, web_agent)

# Knowledge Ingestion Hub
with st.expander("📥 Knowledge Ingestion Hub"):
    col1, col2 = st.columns(2)
    with col1:
        pdf_file = st.file_uploader("Upload PDF Knowledge", type=["pdf"])
        if pdf_file and st.button("Index PDF Source"):
            with st.spinner("📦 Slicing and indexing..."):
                chunks = engine.process_source(file_bytes=pdf_file.read())
                vstore.add_documents(chunks)
                st.session_state.processed_sources.append(f"📄 {pdf_file.name}")
                st.success("Indexed PDF.")
    with col2:
        url_input = st.text_input("Or Ingest Web URL")
        if url_input and st.button("Index URL Source"):
            with st.spinner("🌐 Crawling and indexing..."):
                chunks = engine.process_source(url=url_input)
                vstore.add_documents(chunks)
                st.session_state.processed_sources.append(f"🌐 {url_input}")
                st.success("Indexed URL.")

# Interaction Area
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

query = st.chat_input("Ask about your knowledge base...")
if query:
    st.session_state.history.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)
    
    with st.chat_message("assistant"):
        with st.status("🏗️ Orchestrating Gemini Agentic Flow...", expanded=True) as status:
            try:
                response, rewritten = engine.execute_rag_flow(query)
                st.write(f"🔄 **Query Reformulated**: *{rewritten}*")
                status.update(label="Reasoning Complete", state="complete")
                
                st.markdown(response.content)
                st.session_state.history.append({"role": "assistant", "content": response.content})
            except Exception as e:
                st.error(f"Agentic flow failed: {str(e)}")
