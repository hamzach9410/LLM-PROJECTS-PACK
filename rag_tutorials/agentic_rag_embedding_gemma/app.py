import streamlit as st
import os
from agents_config import get_rag_config
from rag_engine import RAGEngine
from utils import initialize_session, apply_custom_style

# Page configuration
st.set_page_config(
    page_title="Agentic RAG Lab | Gemma",
    page_icon="🔥",
    layout="wide"
)

apply_custom_style()
initialize_session()

st.title("🔥 Agentic RAG Intelligence Lab")
st.markdown("---")

# Initialize Backend
kb, agent = get_rag_config()
engine = RAGEngine(kb, agent)

# Sidebar - Knowledge Management
with st.sidebar:
    col1, col2, col3 = st.columns(3)
    col1.image("google.png")
    col2.image("ollama.png")
    col3.image("agno.png")
    
    st.header("🌐 Knowledge Ingestion")
    new_url = st.text_input("Add PDF URL", placeholder="https://example.com/data.pdf")
    
    if st.button("➕ Ingest Source", use_container_width=True):
        if new_url:
            if new_url not in st.session_state.urls:
                with st.spinner("📥 Indexing document..."):
                    success, msg = engine.add_source(new_url)
                    if success:
                        st.session_state.urls.append(new_url)
                        st.session_state.urls_loaded.add(new_url)
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
            else:
                st.warning("URL already indexed.")
        else:
            st.warning("Please enter a valid URL.")

    if st.session_state.urls:
        st.divider()
        st.subheader("📚 Active Sources")
        for url in st.session_state.urls:
            st.caption(f"• {url}")

# Main Interface
st.markdown("""
### 🧠 Local Intelligence System
This system leverages **EmbeddingGemma** for high-precision semantic search and **Llama 3.2** for reasoning, all running locally via Ollama.
""")

query = st.text_input("🔍 What would you like to know from your knowledge base?", placeholder="Ask a question...")

if st.button("🚀 Analyze & Generate", type="primary"):
    if not query:
        st.warning("Please enter a question.")
    else:
        st.markdown("### 💡 AI Intelligence Output")
        response_container = st.empty()
        full_response = ""
        
        with st.spinner("🧩 Synthesizing answer from knowledge base..."):
            try:
                stream = engine.query_agent(query)
                for chunk in stream:
                    if chunk.content:
                        full_response += chunk.content
                        response_container.markdown(full_response)
            except Exception as e:
                st.error(f"Reasoning failed: {str(e)}")

with st.expander("🛠️ System Architecture"):
    st.info("""
    - **LLM**: Llama 3.2 (Local)
    - **Embedder**: EmbeddingGemma (768 dimensions)
    - **Vector Store**: LanceDB (Serverless)
    - **Framework**: Agno Agentic RAG
    """)
