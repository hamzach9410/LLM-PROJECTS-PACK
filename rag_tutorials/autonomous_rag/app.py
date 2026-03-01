import streamlit as st
import os
import nest_asyncio
from agents_config import get_autonomous_rag_config
from rag_engine import AutonomousEngine
from utils import get_db_url, apply_autonomous_style

# Required for async operations in Streamlit
nest_asyncio.apply()

# Page configuration
st.set_page_config(
    page_title="Autonomous RAG Studio",
    page_icon="🤖",
    layout="wide"
)

apply_autonomous_style()

st.title("🤖 Autonomous RAG Intelligence Studio")
st.markdown("---")

# Sidebar - Configuration
with st.sidebar:
    st.header("⚙️ System Config")
    openai_key = st.text_input("OpenAI API Key", type="password", help="Requires GPT-4o access")
    db_url = st.text_input("Postgres DB URL", value=get_db_url(), help="PgVector compatible database URL")
    
    st.divider()
    st.header("📄 Knowledge Ingestion")
    uploaded_file = st.file_uploader("Upload PDF Knowledge", type=["pdf"])
    
    if uploaded_file and st.button("🛠️ Build Local Knowledge", use_container_width=True):
        if openai_key:
            # Temporary setup to ingest
            kb, agent = get_autonomous_rag_config(openai_key, db_url)
            engine = AutonomousEngine(kb, agent)
            with st.spinner("📦 Indexing into vector database..."):
                success, msg = engine.ingest_pdf(uploaded_file.read())
                if success:
                    st.success(msg)
                else:
                    st.error(msg)
        else:
            st.error("API Key required for embedding.")

if not openai_key:
    st.info("👋 Welcome! Please enter your OpenAI API Key and Database URL in the sidebar to initialize the autonomous agent.")
    st.stop()

# Initialize Backend
try:
    kb, agent = get_autonomous_rag_config(openai_key, db_url)
    engine = AutonomousEngine(kb, agent)
except Exception as e:
    st.error(f"Failed to connect to system: {str(e)}")
    st.stop()

# Main Interface
st.markdown("""
### 🧠 Intelligent Orchestration
This agent autonomously switches between **Internal Knowledge (PgVector)** and **Global Intelligence (DuckDuckGo)** to provide high-fidelity answers.
""")

query = st.text_input("💬 Ask the Autonomous Intelligence:", placeholder="e.g., What are the key findings in the uploaded document?")

if st.button("🔍 Execute Intelligence Search", type="primary"):
    if not query:
        st.warning("Please enter a question.")
    else:
        with st.status("🏗️ Orchestrating search and synthesis...", expanded=True) as status:
            try:
                st.write("🔎 Searching memory and web...")
                response = engine.execute_autonomous_query(query)
                status.update(label="✅ Reasoning Complete", state="complete")
                
                st.markdown("### 📝 Response")
                st.markdown(response.content)
            except Exception as e:
                st.error(f"Autonomous search failed: {str(e)}")

with st.expander("📊 Infrastructure Status"):
    st.write(f"**Storage**: PostgreSQL (Table: `autonomous_rag_storage`)")
    st.write(f"**Vector DB**: PgVector (Collection: `autonomous_rag_docs`)")
    st.write(f"**Model**: GPT-4o Mini")
