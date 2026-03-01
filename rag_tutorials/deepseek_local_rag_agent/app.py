import streamlit as st
import os
from agents_config import get_deepseek_agents
from vector_store import VectorManager
from rag_engine import DeepSeekRAGEngine
from utils import init_deepseek_session, apply_deepseek_style, parse_deepseek_response

# Page configuration
st.set_page_config(
    page_title="DeepSeek Local Intelligence Lab",
    page_icon="🐋",
    layout="wide"
)

apply_deepseek_style()
init_deepseek_session()

st.title("🐋 DeepSeek Local Intelligence Lab")
st.markdown("---")

# Sidebar - Configuration
with st.sidebar:
    st.header("🤖 Model Persona")
    st.session_state.model_version = st.radio(
        "DeepSeek Version",
        ["deepseek-r1:1.5b", "deepseek-r1:7b"],
        help="1.5b for speed, 7b for deeper reasoning."
    )
    
    st.divider()
    st.header("🔍 Retrieval Layer")
    st.session_state.rag_enabled = st.toggle("Enable RAG Ingestion", value=st.session_state.rag_enabled)
    
    if st.session_state.rag_enabled:
        q_url = st.text_input("Qdrant URL", value=st.session_state.qdrant_url)
        q_key = st.text_input("Qdrant API Key", type="password", value=st.session_state.qdrant_api_key)
        st.session_state.qdrant_url = q_url
        st.session_state.qdrant_api_key = q_key
        
        st.session_state.similarity_threshold = st.slider("Similarity Threshold", 0.0, 1.0, 0.7)
        
    st.divider()
    st.header("🌐 Web Fallback")
    st.session_state.use_web_search = st.checkbox("Enable Exa Search Fallback", value=st.session_state.use_web_search)
    if st.session_state.use_web_search:
        st.session_state.exa_api_key = st.text_input("Exa API Key", type="password", value=st.session_state.exa_api_key)

    if st.button("🗑️ Clear Intelligence Memory", use_container_width=True):
        st.session_state.history = []
        st.rerun()

# Main Logic
if st.session_state.rag_enabled and not all([st.session_state.qdrant_url, st.session_state.qdrant_api_key]):
    st.info("👋 Welcome! Please configure Qdrant settings in the sidebar to activate the local RAG system.")
    st.stop()

# Initialize Backend
v_manager = VectorManager(st.session_state.qdrant_url, st.session_state.qdrant_api_key)
v_manager.setup_collection()
vstore = v_manager.get_vectorstore()

rag_agent, web_agent = get_deepseek_agents(
    st.session_state.model_version,
    st.session_state.exa_api_key if st.session_state.use_web_search else None
)
engine = DeepSeekRAGEngine(vstore, rag_agent, web_agent)

# Data Ingestion Area
if st.session_state.rag_enabled:
    with st.expander("📥 Knowledge Ingestion Hub"):
        col1, col2 = st.columns(2)
        with col1:
            pdf_file = st.file_uploader("Upload PDF Knowledge", type=["pdf"])
            if pdf_file and st.button("Index PDF"):
                with st.spinner("Indexing..."):
                    chunks = engine.process_document(file_bytes=pdf_file.read())
                    v_manager.get_vectorstore().add_documents(chunks)
                    st.session_state.processed_sources.append(f"📄 {pdf_file.name}")
                    st.success("PDF Indexed!")
        with col2:
            url_input = st.text_input("Or Ingest Web URL")
            if url_input and st.button("Index URL"):
                with st.spinner("Indexing..."):
                    chunks = engine.process_document(url=url_input)
                    v_manager.get_vectorstore().add_documents(chunks)
                    st.session_state.processed_sources.append(f"🌐 {url_input}")
                    st.success("URL Indexed!")

# Conversation Interface
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

query = st.chat_input("Ask about your knowledge base...")
if query:
    st.session_state.history.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)
    
    with st.chat_message("assistant"):
        with st.status("🐋 DeepSeek is reasoning...", expanded=True) as status:
            try:
                response = engine.run_rag_query(query, threshold=st.session_state.similarity_threshold)
                status.update(label="Reasoning Complete", state="complete")
                
                thinking, answer = parse_deepseek_response(response.content)
                if thinking:
                    with st.expander("🤔 View Thinking Process"):
                        st.markdown(f'<div class="thinking-container">{thinking}</div>', unsafe_allow_html=True)
                
                st.markdown(answer)
                st.session_state.history.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"Intelligence processing failed: {str(e)}")
