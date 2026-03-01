import streamlit as st
import os
import json
from agents_config import ContextualConfig
from rag_engine import ContextualEngine
from utils import init_contextual_session, apply_contextual_style, post_process_answer

# Page configuration
st.set_page_config(
    page_title="Contextual Intelligence Hub",
    page_icon="🧬",
    layout="wide"
)

apply_contextual_style()
init_contextual_session()

st.title("🧬 Contextual AI Intelligence Hub")
st.markdown("---")

# Sidebar - API Setup
with st.sidebar:
    st.header("🔑 SDK Configuration")
    if not st.session_state.api_key_submitted:
        with st.form("api_form"):
            api_key = st.text_input("Contextual API Key", type="password")
            base_url = st.text_input("Base URL", value=st.session_state.base_url)
            
            if st.form_submit_button("Verify & Activate", use_container_width=True):
                if ContextualConfig.verify_credentials(api_key, base_url):
                    st.session_state.contextual_api_key = api_key
                    st.session_state.base_url = base_url
                    st.session_state.api_key_submitted = True
                    st.success("API Verified!")
                    st.rerun()
                else:
                    st.error("Invalid credentials.")
    else:
        st.success("✅ SDK Active")
        if st.button("Reset Session", use_container_width=True):
            st.session_state.clear()
            st.rerun()

if not st.session_state.api_key_submitted:
    st.info("👋 Welcome! Please enter your Contextual AI API key in the sidebar to initialize the platform.")
    st.stop()

# Initialize Engine
config = ContextualConfig(st.session_state.contextual_api_key, st.session_state.base_url)
engine = ContextualEngine(config.get_client())

# Main Interface Tabs
tab1, tab2, tab3 = st.tabs(["🏗️ Infrastructure", "💬 Chat Interface", "🛡️ Evaluation"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("1. Datastore Management")
        if not st.session_state.datastore_id:
            ds_name = st.text_input("Datastore Name", value="contextual_lab_ds")
            if st.button("Create Datastore"):
                ds_id = engine.create_datastore(ds_name)
                if ds_id:
                    st.session_state.datastore_id = ds_id
                    st.success(f"Created: {ds_id}")
        else:
            st.success(f"Active Datastore: {st.session_state.datastore_id}")
            
        st.divider()
        st.subheader("2. Document Ingestion")
        files = st.file_uploader("Upload Knowledge (PDF/TXT)", accept_multiple_files=True)
        if files and st.session_state.datastore_id:
            if st.button("Ingest Knowledge"):
                contents = [f.getvalue() for f in files]
                names = [f.name for f in files]
                with st.spinner("📦 Indexing documents..."):
                    ids = engine.upload_docs(st.session_state.datastore_id, contents, names)
                    if ids:
                        st.success(f"Ingested {len(ids)} documents.")

    with col2:
        st.subheader("3. Agent Orchestration")
        if not st.session_state.agent_id and st.session_state.datastore_id:
            agent_name = st.text_input("Agent Name", value="Intelligence Analyst")
            if st.button("Deploy Agent"):
                a_id = engine.create_agent(agent_name, "RAG analyst for knowledge hub", st.session_state.datastore_id)
                if a_id:
                    st.session_state.agent_id = a_id
                    st.success(f"Deployed: {a_id}")
        elif st.session_state.agent_id:
            st.success(f"Active Agent: {st.session_state.agent_id}")

with tab2:
    if st.session_state.agent_id:
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
        
        query = st.chat_input("Ask about your documents...")
        if query:
            st.session_state.chat_history.append({"role": "user", "content": query})
            with st.chat_message("user"):
                st.markdown(query)
            
            with st.chat_message("assistant"):
                answer, raw = engine.query(st.session_state.agent_id, query)
                processed = post_process_answer(answer)
                st.markdown(processed)
                st.session_state.chat_history.append({"role": "assistant", "content": processed})
                st.session_state.last_raw_response = raw
                st.session_state.last_user_query = query
    else:
        st.warning("Please configure your infrastructure in the first tab to enable chat.")

with tab3:
    st.subheader("🔍 Retrieval Diagnostics")
    if st.session_state.last_raw_response:
        st.json(st.session_state.last_raw_response)
    else:
        st.info("No query diagnostics available yet.")
