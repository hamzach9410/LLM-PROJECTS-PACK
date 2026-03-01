import streamlit as st
import os
from rag_config import HybridRAGConfig
from rag_engine import HybridRAGEngine
from utils import init_hybrid_session, apply_premium_style, run_fallback_query

# Page configuration
st.set_page_config(
    page_title="Hybrid Intelligence Lab",
    page_icon="👀",
    layout="wide"
)

apply_premium_style()
init_hybrid_session()

st.title("👀 Hybrid RAG Intelligence Lab")
st.markdown("---")

# Sidebar - Configuration
with st.sidebar:
    st.header("🔑 Multi-Model Config")
    o_key = st.text_input("OpenAI Key", type="password", value=st.session_state.openai_key)
    a_key = st.text_input("Anthropic Key", type="password", value=st.session_state.anthropic_key)
    c_key = st.text_input("Cohere Key", type="password", value=st.session_state.cohere_key)
    db_url = st.text_input("Database URL", value=st.session_state.db_url)
    
    if st.button("🚀 Initialize System", use_container_width=True):
        if all([o_key, a_key, c_key, db_url]):
            st.session_state.openai_key = o_key
            st.session_state.anthropic_key = a_key
            st.session_state.cohere_key = c_key
            st.session_state.db_url = db_url
            
            config_mgr = HybridRAGConfig(o_key, a_key, c_key, db_url)
            st.session_state.rag_config = config_mgr.get_raglite_config()
            st.success("Intelligence engine ready!")
        else:
            st.error("Missing credentials.")

# Main Interface
if not st.session_state.rag_config:
    st.info("👋 Welcome! Please configure your multi-model credentials in the sidebar to activate the hybrid RAG platform.")
    st.stop()

# Initialize Engine
engine = HybridRAGEngine(st.session_state.rag_config)

# Document Ingestion
st.subheader("📥 Strategic Knowledge Ingestion")
files = st.file_uploader("Upload PDF Documents", type=["pdf"], accept_multiple_files=True)

if files:
    for f in files:
        if st.button(f"Index {f.name}"):
            with st.spinner(f"Splitting and indexing {f.name}..."):
                temp_path = f"tmp_{f.name}"
                with open(temp_path, "wb") as tmp:
                    tmp.write(f.getvalue())
                success, msg = engine.ingest_document(temp_path)
                os.remove(temp_path)
                if success:
                    st.success(msg)
                    st.session_state.documents_ready = True
                else:
                    st.error(msg)

# Conversation Area
if st.session_state.documents_ready:
    st.divider()
    for user_msg, assist_msg in st.session_state.chat_history:
        with st.chat_message("user"): st.markdown(user_msg)
        with st.chat_message("assistant"): st.markdown(assist_msg)
        
    query = st.chat_input("Ask about your documents...")
    if query:
        with st.chat_message("user"): st.markdown(query)
        
        with st.chat_message("assistant"):
            resp_placeholder = st.empty()
            full_resp = ""
            
            # 1. Search Check
            with st.spinner("🔍 Executing hybrid search & reranking..."):
                ranked_chunks = engine.search_and_rank(query)
                
            if not ranked_chunks:
                st.info("No relevant context found. Falling back to global knowledge.")
                full_resp = run_fallback_query(query, st.session_state.anthropic_key)
                resp_placeholder.markdown(full_resp)
            else:
                # 2. Sequential Synthesis
                history_formatted = [] # Simplified for demo
                stream = engine.stream_rag_response(query, history_formatted)
                for chunk in stream:
                    full_resp += chunk
                    resp_placeholder.markdown(full_resp + "▌")
                resp_placeholder.markdown(full_resp)
            
            st.session_state.chat_history.append((query, full_resp))
else:
    st.info("Please upload and index documents to enable the intelligence assistant.")
