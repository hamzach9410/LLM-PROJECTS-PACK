import streamlit as st
import os
from agents_config import get_qwen_rag_agent, get_web_search_agent
from vector_store import QwenVectorManager
from rag_engine import QwenRAGLogic
from utils import init_qwen_session, apply_qwen_style, show_model_info

st.set_page_config(page_title="Qwen Strategic Lab", layout="wide")
apply_qwen_style()
init_qwen_session()

st.title("🐋 Qwen 2.5 Strategic Intelligence Lab")
show_model_info()
st.markdown("---")

# Sidebar - Settings
with st.sidebar:
    st.header("⚙️ Core Intelligence")
    m_choice = st.radio("Model Version", ["qwen2.5:1.5b", "gemma:2b", "deepseek-r1:1.5b"])
    st.session_state.model_version = m_choice
    
    st.divider()
    st.header("🌍 Web Search Fallback")
    e_key = st.text_input("Exa API Key", type="password", value=st.session_state.exa_key)
    st.session_state.exa_key = e_key
    use_web = st.checkbox("Enable Web Fallback", value=st.session_state.use_web)
    st.session_state.use_web = use_web
    
    if st.button("✨ Reset Lab Session", use_container_width=True):
        st.session_state.history = []
        st.rerun()

# Initialize Engines
v_mgr = QwenVectorManager()
rag_logic = QwenRAGLogic(st.session_state.vector_store)

# Ingestion Panel
with st.expander("📥 Knowledge Ingestion Hub", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        pdfs = st.file_uploader("Upload PDFs", accept_multiple_files=True, type='pdf')
    with col2:
        url = st.text_input("Ingest URL")
        
    if st.button("🚀 Process Intelligence Data"):
        all_splits = []
        if pdfs:
            for f in pdfs:
                if f.name not in st.session_state.processed_docs:
                    splits = rag_logic.process_pdf(f.getvalue(), f.name)
                    all_splits.extend(splits)
                    st.session_state.processed_docs.append(f.name)
        if url and url not in st.session_state.processed_docs:
            splits = rag_logic.process_web(url)
            all_splits.extend(splits)
            st.session_state.processed_docs.append(url)
            
        if all_splits:
            with st.spinner("Syncing to local vector cluster..."):
                v_mgr.ensure_collection()
                vs = v_mgr.get_vector_store()
                vs.add_documents(all_splits)
                st.session_state.vector_store = vs
                st.success(f"Synchronized {len(all_splits)} intelligence fragments.")

# Q&A Interface
st.divider()
query = st.chat_input("Ask about the technical frameworks...")

if query:
    st.session_state.history.append({"role": "user", "content": query})
    with st.chat_message("user"): st.markdown(query)
    
    with st.chat_message("assistant"):
        with st.spinner("🔍 Executing multi-stage reasoning..."):
            context = ""
            source_docs = []
            
            # 1. Local RAG Check
            if st.session_state.vector_store:
                context, source_docs = rag_logic.retrieve_context(query)
                
            # 2. Web Fallback
            if not context and st.session_state.use_web and st.session_state.exa_key:
                st.info("No local documentation found. Activating web search intelligence...")
                web_agent = get_web_search_agent(st.session_state.exa_key)
                context = f"Web Intel: {web_agent.run(query).content}"
                
            # 3. Final Synthesis
            rag_agent = get_qwen_rag_agent(st.session_state.model_version)
            full_prompt = f"Context: {context}\n\nQuery: {query}" if context else query
            resp = rag_agent.run(full_prompt)
            
            st.markdown(resp.content)
            if source_docs:
                with st.expander("📚 Cited Local Sources"):
                    for d in source_docs:
                        st.caption(f"Source: {d.metadata.get('source')} | Fragment: {d.page_content[:150]}...")
            
            st.session_state.history.append({"role": "assistant", "content": resp.content})
