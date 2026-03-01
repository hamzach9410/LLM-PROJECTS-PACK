import streamlit as st
import time
from rag_engine import RAGServiceEngine
from utils import init_raas_session, apply_raas_style

st.set_page_config(page_title="RAG-as-a-Service", page_icon="🔗", layout="wide")
apply_raas_style()
init_raas_session()

st.title("🔗 Industrial RAG-as-a-Service (RaaS)")
st.markdown("---")

# Sidebar - Key Management
with st.sidebar:
    st.header("🔑 API Infrastructure")
    r_key = st.text_input("Ragie.ai API Key", type="password", value=st.session_state.ragie_key)
    a_key = st.text_input("Anthropic API Key", type="password", value=st.session_state.anthropic_key)
    
    if st.button("🚀 Deploy RAG Engine"):
        if r_key and a_key:
            st.session_state.ragie_key = r_key
            st.session_state.anthropic_key = a_key
            st.session_state.engine = RAGServiceEngine(r_key, a_key)
            st.success("RAG Engine Deployed.")
        else:
            st.error("Infrastructure keys missing.")

# Main Interface
if not st.session_state.engine:
    st.info("👋 Welcome! Please configure and deploy your RAG infrastructure in the sidebar to start document indexing.")
    st.stop()

# Ingestion Section
st.subheader("📥 Strategic Knowledge Ingestion")
doc_url = st.text_input("Source Document URL (Public PDF/HTML)")
doc_name = st.text_input("Internal Identifier (Optional)")

if st.button("Index Source"):
    if doc_url:
        with st.spinner("Pushing to Ragie.ai managed index..."):
            try:
                st.session_state.engine.ingest_new_source(doc_url, doc_name)
                time.sleep(3) # Short buffer for cloud indexing
                st.session_state.indexed = True
                st.success("Knowledge fragment synchronized.")
            except Exception as e:
                st.error(f"Sync failed: {str(e)}")

# Intelligence Interaction
if st.session_state.indexed:
    st.divider()
    st.subheader("🔍 Intelligence Query Interface")
    query = st.chat_input("Ask about the synchronized documentation...")
    
    if query:
        with st.chat_message("user"): st.markdown(query)
        with st.chat_message("assistant"):
            with st.spinner("Retrieving and synthesizing fragments..."):
                try:
                    ans = st.session_state.engine.run_strategic_query(query)
                    st.markdown(ans)
                    st.session_state.chat_history.append((query, ans))
                except Exception as e:
                    st.error(f"Reasoning failed: {str(e)}")
else:
    st.info("Index at least one source to activate the intelligence interface.")
