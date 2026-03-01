import streamlit as st
from rag_config import PharmaConfig
from rag_engine import PharmaRAGEngine
from utils import init_pharma_session, apply_pharma_style

st.set_page_config(page_title="PharmaQuery Lab", page_icon="🧬", layout="wide")
apply_pharma_style()
init_pharma_session()

st.title("🧬 PharmaQuery: Strategic Research Hub")
st.markdown("---")

# Sidebar - Key Mgt
with st.sidebar:
    st.header("🔑 Intelligence Keys")
    g_key = st.text_input("Gemini API Key", type="password", value=st.session_state.gemini_key)
    if st.button("Activate Lab Core"):
        if g_key:
            st.session_state.gemini_key = g_key
            st.success("Lab Core Activated.")
        else:
            st.error("API Key Required.")

# Infrastructure Lock
if not st.session_state.gemini_key:
    st.info("👋 Welcome! Please activate the laboratory core with your Gemini API key in the sidebar.")
    st.stop()

# Initialize Engine
cfg = PharmaConfig(st.session_state.gemini_key)
engine = PharmaRAGEngine(cfg, cfg.get_vector_db())

# Document Ingestion
with st.sidebar:
    st.divider()
    st.header("📥 Research Ingestion")
    pdfs = st.file_uploader("Upload Pharma PDFs", type=['pdf'], accept_multiple_files=True)
    if st.button("Index Research"):
        if pdfs:
            with st.spinner("Processing clinical data..."):
                engine.ingest_pdfs(pdfs)
                st.session_state.ready = True
                st.success("Research Indexed.")

# Research Q&A
st.subheader("🔍 Strategic Research Query")
query = st.text_area("Enter your research hypothesis or question:", placeholder="e.g., Mechanism of action for novel GLP-1 agonists...")

if st.button("Execute Analysis"):
    if query:
        with st.spinner("Analyzing pharmaceutical fragments..."):
            try:
                res = engine.query_vault(query)
                st.markdown("### 📊 Research Synthesis")
                st.markdown(res)
                st.session_state.history.append((query, res))
            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")
    else:
        st.warning("Please enter a research query.")