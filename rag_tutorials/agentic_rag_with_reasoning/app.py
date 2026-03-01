import streamlit as st
import os
from agents_config import get_rag_reasoning_config
from rag_engine import ReasoningEngine
from utils import initialize_reasoning_session, apply_styling

# Page configuration
st.set_page_config(
    page_title="Reasoning RAG Hub",
    page_icon="🧐",
    layout="wide"
)

apply_styling()
initialize_reasoning_session()

st.title("🧐 Agentic Reasoning RAG Hub")
st.markdown("---")

# API Keys Configuration
with st.sidebar:
    st.header("🔑 Authentication")
    google_key = st.text_input("Google API Key", type="password", value=os.getenv("GOOGLE_API_KEY", ""))
    openai_key = st.text_input("OpenAI API Key", type="password", value=os.getenv("OPENAI_API_KEY", ""))
    
    st.divider()
    st.header("📚 Knowledge Management")
    new_url = st.text_input("Add Source URL", placeholder="https://example.com/article")
    
    if st.button("➕ Add Source", use_container_width=True):
        if google_key and openai_key:
            if new_url and new_url not in st.session_state.knowledge_urls:
                st.session_state.knowledge_urls.append(new_url)
                st.success("Added to queue!")
                st.rerun()
        else:
            st.error("Please provide both API keys first.")

    if st.session_state.knowledge_urls:
        st.subheader("Current Sources")
        for url in st.session_state.knowledge_urls:
            st.caption(f"• {url}")

# Main Logic
if not google_key or not openai_key:
    st.info("👋 Welcome! Please enter your Google and OpenAI API keys in the sidebar to activate the reasoning agent.")
    st.stop()

# Initialize Backend
kb, agent = get_rag_reasoning_config(google_key, openai_key)
engine = ReasoningEngine(kb, agent)

# Auto-load initial sources
for url in st.session_state.knowledge_urls:
    if url not in st.session_state.urls_loaded:
        with st.spinner(f"📥 Indexing {url}..."):
            success, msg = engine.add_knowledge_source(url)
            if success:
                st.session_state.urls_loaded.add(url)

# Interaction Area
st.subheader("🤔 Deep Reasoning Query")
query = st.text_area("What would you like the agent to analyze?", value=st.session_state.query, height=100)

if st.button("🚀 Process with Deep Reasoning", type="primary"):
    if not query:
        st.warning("Please enter a query.")
    else:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### 🧠 Reasoning Chain")
            reasoning_placeholder = st.empty()
        
        with col2:
            st.markdown("### 💡 Final Synthesis")
            answer_placeholder = st.empty()
        
        full_reasoning = ""
        full_answer = ""
        citations = []
        
        try:
            with st.spinner("Processing..."):
                stream = engine.run_reasoning_query(query)
                for chunk in stream:
                    # Update reasoning display
                    if hasattr(chunk, 'reasoning_content') and chunk.reasoning_content:
                        full_reasoning = chunk.reasoning_content
                        reasoning_placeholder.markdown(f'<div class="reasoning-box">{full_reasoning}</div>', unsafe_allow_html=True)
                    
                    # Update answer display
                    if hasattr(chunk, 'content') and chunk.content and isinstance(chunk.content, str):
                        full_answer += chunk.content
                        answer_placeholder.markdown(full_answer)
                    
                    # Collect citations
                    if hasattr(chunk, 'citations') and chunk.citations:
                        if hasattr(chunk.citations, 'urls') and chunk.citations.urls:
                            citations = chunk.citations.urls

            if citations:
                st.divider()
                st.subheader("📚 Verified Sources")
                for cite in citations:
                    st.markdown(f"- [{cite.title or cite.url}]({cite.url})")
                    
        except Exception as e:
            st.error(f"Reasoning process failed: {str(e)}")
