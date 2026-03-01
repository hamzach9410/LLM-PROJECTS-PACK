import streamlit as st
from rag_config import RoutingConfig
from router_engine import MultiSourceRouter
from utils import init_routing_session, apply_routing_style, process_pdf_fragment

st.set_page_config(page_title="Data Router Hub", layout="wide")
apply_routing_style()
init_routing_session()

st.title("📠 Multi-Source Intelligence Router")
st.markdown("---")

# Sidebar - Infra Cluster
with st.sidebar:
    st.header("⚡ Core Infrastructure")
    o_key = st.text_input("OpenAI API Key", type="password", value=st.session_state.openai_key)
    q_url = st.text_input("Qdrant URL", value=st.session_state.qdrant_url)
    q_key = st.text_input("Qdrant API Key", type="password", value=st.session_state.qdrant_key)
    
    if st.button("🚀 Sync Cluster"):
        if o_key and q_url and q_key:
            st.session_state.openai_key = o_key
            st.session_state.qdrant_url = q_url
            st.session_state.qdrant_key = q_key
            st.success("Cluster Synchronized.")

# Infra Guard
if not all([st.session_state.openai_key, st.session_state.qdrant_url, st.session_state.qdrant_key]):
    st.info("👋 Welcome! Please synchronize your data cluster in the sidebar to begin multi-source routing.")
    st.stop()

# Initialize
cfg = RoutingConfig(st.session_state.openai_key, st.session_state.qdrant_url, st.session_state.qdrant_key)
router = MultiSourceRouter(cfg)

# Ingestion Tabs
st.subheader("📥 Data Silo Ingestion")
t1, t2, t3 = st.tabs(["📦 Products", "🛠️ Support", "💰 Finance"])

def handle_upload(col, files):
    if files:
        with st.spinner(f"Fragmenting data for {col}..."):
            all_splits = []
            for f in files:
                all_splits.extend(process_pdf_fragment(f))
            vs = cfg.get_vector_store(col)
            vs.add_documents(all_splits)
            st.success(f"{col} silo updated.")

with t1:
    f1 = st.file_uploader("Product Specs PDFs", type=['pdf'], accept_multiple_files=True, key="f1")
    if st.button("Index Products"): handle_upload("products", f1)
with t2:
    f2 = st.file_uploader("Support/FAQ PDFs", type=['pdf'], accept_multiple_files=True, key="f2")
    if st.button("Index Support"): handle_upload("support", f2)
with t3:
    f3 = st.file_uploader("Financial Report PDFs", type=['pdf'], accept_multiple_files=True, key="f3")
    if st.button("Index Finance"): handle_upload("finance", f3)

# Routing Dashboard
st.divider()
st.subheader("🔍 Intelligent Query Routing")
query = st.text_input("Enter cross-silo query:", placeholder="e.g., What was the Q3 revenue for the X1 model?")

if st.button("Execute Routing Cycle"):
    if query:
        with st.spinner("Classifying query intent..."):
            source = router.route_query(query)
            
            if source in ["products", "support", "finance"]:
                st.info(f"🎯 Route Target: **{source.upper()}** silo")
                with st.spinner(f"Executing RAG in {source} silo..."):
                    res = router.execute_rag(query, source)
                    st.markdown("### 📊 Intent-Specific Result")
                    st.write(res["answer"])
            else:
                st.warning("⚠️ No internal silo target matched. Initiating web fallback...")
                with st.spinner("Executing external research agent..."):
                    res = router.web_fallback(query)
                    st.markdown("### 🌐 External Research Result")
                    st.write(res)
