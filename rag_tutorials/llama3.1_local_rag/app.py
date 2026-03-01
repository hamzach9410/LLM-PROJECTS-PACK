import streamlit as st
from rag_config import OllamaConfig
from rag_engine import LocalRAGEngine
from utils import init_local_session, apply_local_style

st.set_page_config(page_title="Local Web Intelligence", layout="wide")
apply_local_style()
init_local_session()

st.title("🌐 Local Web Intelligence Hub")
st.markdown("---")

# Configuration
with st.sidebar:
    st.header("⚙️ Local Core")
    model = st.text_input("Ollama Model", value="llama3.1")
    url = st.text_input("Ollama Endpoint", value="http://127.0.0.1:11434")
    config = OllamaConfig(model, url)

# Initialize Engine
engine = LocalRAGEngine(config)

# Ingestion
st.subheader("📥 Strategic Knowledge Ingestion")
web_url = st.text_input("Enter target URL for intelligence harvesting")

if web_url and st.button("🚀 Harvest Knowledge"):
    with st.spinner(f"Crawling {web_url}..."):
        try:
            engine.ingest_web_page(web_url)
            st.session_state.url_loaded = True
            st.success("Knowledge stored in local vector vault.")
        except Exception as e:
            st.error(f"Harvest failed: {str(e)}")

# Q&A Logic
if st.session_state.url_loaded:
    st.divider()
    query = st.chat_input("Ask about the harvested intelligence...")
    if query:
        with st.chat_message("user"): st.markdown(query)
        with st.chat_message("assistant"):
            with st.spinner("Analyzing local fragments..."):
                answer = engine.query(query)
                st.markdown(answer)
                st.session_state.history.append((query, answer))
else:
    st.info("Input a URL and harvest knowledge to begin local analysis.")
