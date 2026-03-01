import streamlit as st
import os
from rag_config import LocalHybridConfig
from rag_engine import LocalHybridRAGEngine
from utils import init_local_hybrid_session, apply_local_hybrid_style

st.set_page_config(page_title="Local Hybrid Intelligence", layout="wide")
apply_local_hybrid_style()
init_local_hybrid_session()

st.title("🖥️ Local Hybrid Intelligence Studio")
st.markdown("---")

# Sidebar - GGUF Config
with st.sidebar:
    st.header("⚙️ Local GGUF Core")
    l_path = st.text_input("LLM GGUF Path", placeholder="/path/to/llama.gguf", value=st.session_state.llm_path)
    e_path = st.text_input("Embedder GGUF Path", placeholder="/path/to/embedder.gguf", value=st.session_state.embedder_path)
    db_u = st.text_input("Database URL", value=st.session_state.db_url)
    
    if st.button("🚀 Initialize Core", use_container_width=True):
        if all([l_path, e_path, db_u]):
            st.session_state.llm_path = l_path
            st.session_state.embedder_path = e_path
            st.session_state.db_url = db_u
            
            cfg_mgr = LocalHybridConfig(db_u, l_path, e_path)
            st.session_state.rag_config = cfg_mgr.get_raglite_config()
            st.success("Core Initialized.")

# Main Logic
if not st.session_state.rag_config:
    st.info("👋 Welcome! Please provide the absolute paths to your local GGUF models in the sidebar to begin.")
    st.stop()

# Initialize Engine
engine = LocalHybridRAGEngine(st.session_state.rag_config)

# Ingestion Hub
st.subheader("📥 Local Knowledge Ingestion")
files = st.file_uploader("Upload PDF Documents", type=["pdf"], accept_multiple_files=True)

if files:
    for f in files:
        if st.button(f"Index {f.name}"):
            with st.spinner(f"Indexing {f.name} locally..."):
                tmp_fn = f"tmp_{f.name}"
                with open(tmp_fn, "wb") as tmp:
                    tmp.write(f.getvalue())
                success, msg = engine.ingest_document(tmp_fn)
                os.remove(tmp_fn)
                if success:
                    st.success(msg)
                    st.session_state.docs_loaded = True

# Conversation
if st.session_state.docs_loaded:
    st.divider()
    for u, a in st.session_state.chat_history:
        with st.chat_message("user"): st.markdown(u)
        with st.chat_message("assistant"): st.markdown(a)
        
    query = st.chat_input("Ask about your private intelligence storage...")
    if query:
        with st.chat_message("user"): st.markdown(query)
        with st.chat_message("assistant"):
            resp_box = st.empty()
            full = ""
            
            with st.spinner("Executing local hybrid search..."):
                results = engine.search_and_rank(query)
                
            if not results:
                st.warning("No relevant local context found.")
            else:
                stream = engine.stream_response(query, []) # Simplified
                for chunk in stream:
                    full += chunk
                    resp_box.markdown(full + "▌")
                resp_box.markdown(full)
                st.session_state.chat_history.append((query, full))
else:
    st.info("Ingest documents to activate the intelligence assistant.")
