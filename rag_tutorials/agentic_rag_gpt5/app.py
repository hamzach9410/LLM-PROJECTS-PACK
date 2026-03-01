import streamlit as st
import os
from agents_config import get_gpt5_agent
from rag_engine import GPT5RAGEngine
from utils import init_gpt5_session, apply_gpt5_style

# Page configuration
st.set_page_config(
    page_title="GPT-5 Intelligence Lab",
    page_icon="🧠",
    layout="wide"
)

apply_gpt5_style()
init_gpt5_session()

st.title("🧠 GPT-5 Strategic Intelligence Lab")
st.markdown("---")

# Sidebar - Configuration
with st.sidebar:
    st.header("🔑 Intelligence Core")
    o_key = st.text_input("OpenAI API Key", type="password", value=st.session_state.openai_api_key)
    st.session_state.openai_api_key = o_key
    
    st.divider()
    st.header("🌐 Source Ingestion")
    new_url = st.text_input("Add URL to Knowledge Base")
    if st.button("➕ Index URL", use_container_width=True):
        if new_url and new_url not in st.session_state.knowledge_urls:
            st.session_state.knowledge_urls.append(new_url)
            st.success(f"Queued: {new_url}")

# Main Logic
if not st.session_state.openai_api_key:
    st.info("👋 Welcome! Please configure your OpenAI API key in the sidebar to activate the intelligence lab.")
    st.stop()

# Initialize Backend
agent, kb = get_gpt5_agent(st.session_state.openai_api_key)
engine = GPT5RAGEngine(agent, kb)

# Ensure initial URLs are loaded
for url in st.session_state.knowledge_urls:
    if url not in st.session_state.urls_loaded:
        with st.spinner(f"Indexing {url}..."):
            engine.add_knowledge_url(url)
            st.session_state.urls_loaded.add(url)

# Display Knowledge Base
if st.session_state.knowledge_urls:
    st.subheader("📚 Active Knowledge Base")
    st.caption(", ".join(st.session_state.knowledge_urls))

# Prompt Interface
st.divider()
query = st.chat_input("Ask about the protocols and strategic frameworks...")

if query:
    st.session_state.chat_history.append({"role": "user", "content": query})
    with st.chat_message("user"): st.markdown(query)
    
    with st.chat_message("assistant"):
        resp_placeholder = st.empty()
        full_resp = ""
        
        with st.spinner("🔍 Analyzing knowledge fragments..."):
            stream = engine.query_agent_stream(query)
            for chunk in stream:
                if hasattr(chunk, 'content') and chunk.content:
                    full_resp += str(chunk.content)
                    resp_placeholder.markdown(full_resp + "▌")
            resp_placeholder.markdown(full_resp)
            st.session_state.chat_history.append({"role": "assistant", "content": full_resp})
