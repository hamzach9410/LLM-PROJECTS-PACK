import streamlit as st
from agents_config import CohereAgentConfig
from vector_store import QdrantManager
from rag_engine import CohereRAGEngine
from utils import init_cohere_session, apply_cohere_style

st.set_page_config(page_title="Cohere Strategic Lab", layout="wide")
apply_cohere_style()
init_cohere_session()

st.title("⌘ Cohere Strategic Intelligence Lab")
st.markdown("---")

# Sidebar - Infra
with st.sidebar:
    st.header("🔑 Model Infrastructure")
    c_key = st.text_input("Cohere API Key", type="password", value=st.session_state.cohere_key)
    q_url = st.text_input("Qdrant Cluster URL", value=st.session_state.qdrant_url)
    q_key = st.text_input("Qdrant API Key", type="password", value=st.session_state.qdrant_key)
    
    if st.button("🚀 Initialize Ecosystem", use_container_width=True):
        if all([c_key, q_url, q_key]):
            st.session_state.cohere_key = c_key
            st.session_state.qdrant_url = q_url
            st.session_state.qdrant_key = q_key
            st.success("Ecosystem Ready.")

# Connectivity
if not all([st.session_state.cohere_key, st.session_state.qdrant_url, st.session_state.qdrant_key]):
    st.info("👋 Welcome! Please configure your Cohere and Qdrant credentials in the sidebar to activate the intelligence lab.")
    st.stop()

# Initialize Backend
cfg = CohereAgentConfig(st.session_state.cohere_key)
v_mgr = QdrantManager(st.session_state.qdrant_url, st.session_state.qdrant_key)
engine = CohereRAGEngine(cfg.get_chat_model(), v_mgr.get_vector_store(cfg.get_embeddings()), cfg.get_fallback_agent())

# Ingestion
st.subheader("📥 Strategic Knowledge Ingestion")
pdf_file = st.file_uploader("Upload Intelligence PDF", type=['pdf'])
if pdf_file and not st.session_state.ready:
    with st.spinner("Indexing document fragments..."):
        splits = engine.process_pdf(pdf_file.getvalue())
        v_mgr.ensure_collection()
        v_mgr.get_vector_store(cfg.get_embeddings()).add_documents(splits)
        st.session_state.ready = True
        st.success("Indexing Complete.")

# Q&A Logic
if st.session_state.ready:
    st.divider()
    query = st.chat_input("Analyze the document or search the web...")
    if query:
        with st.chat_message("user"): st.markdown(query)
        with st.chat_message("assistant"):
            with st.spinner("🔍 Executing agentic research..."):
                answer, sources = engine.execute_query(query)
                st.markdown(answer)
                if sources:
                    with st.expander("📚 Sources"):
                        for s in sources: st.caption(s.page_content[:200] + "...")
                st.session_state.chat_history.append((query, answer))
else:
    st.info("Upload a document to activate the strategic assistant.")
