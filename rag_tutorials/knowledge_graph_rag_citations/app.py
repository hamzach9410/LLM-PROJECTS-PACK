import streamlit as st
import os
from graph_config import KnowledgeGraphManager
from rag_engine import GraphRAGEngine
from utils import init_graph_session, apply_graph_style

st.set_page_config(page_title="Graph Intelligence Studio", layout="wide")
apply_graph_style()
init_graph_session()

st.title("🔍 Knowledge Graph Intelligence Studio")
st.markdown("---")

# Sidebar - Config
with st.sidebar:
    st.header("⚙️ Graph Core")
    uri = st.text_input("Neo4j Bolt URI", value=st.session_state.neo4j_uri)
    user = st.text_input("Neo4j User", value=st.session_state.neo4j_user)
    pwd = st.text_input("Neo4j Password", type="password")
    
    st.divider()
    model = st.selectbox("Intelligence Model", ["llama3.1", "mistral"])
    
    if st.button("🗑️ Clear Research Graph", use_container_width=True):
        if all([uri, user, pwd]):
            gm = KnowledgeGraphManager(uri, user, pwd)
            gm.clear_graph()
            gm.close()
            st.session_state.graph_ready = False
            st.session_state.indexed_docs = []
            st.success("Graph Purged.")

# Connectivity Check
if not all([uri, user, pwd]):
    st.warning("👋 Please provide Neo4j credentials in the sidebar to activate the research studio.")
    st.stop()

# Initialize Engines
gm = KnowledgeGraphManager(uri, user, pwd)
engine = GraphRAGEngine(os.getenv("OLLAMA_HOST", "http://localhost:11434"), gm)

# Main UI Tabs
tab_ingest, tab_ask, tab_viz = st.tabs(["📄 Ingestion Hub", "❓ Strategic Q&A", "📊 Graph Insights"])

with tab_ingest:
    st.subheader(" strategic Knowledge Ingestion")
    doc_name = st.text_input("Document Category/Name", value="Corporate Report")
    doc_text = st.text_area("Paste Intelligence Data", height=200)
    
    if st.button("🔨 Extract & Sync to Graph", type="primary"):
        with st.spinner("Extracting multi-hop entities..."):
            engine.extract_and_index(doc_text, doc_name, model=model)
            st.session_state.graph_ready = True
            st.session_state.indexed_docs.append(doc_name)
            st.success("Sync Complete.")

with tab_ask:
    if not st.session_state.graph_ready:
        st.info("Ingest documentation to enable strategic querying.")
    else:
        st.subheader("💡 Ask with Verifiable Citations")
        query = st.text_input("Strategic Question")
        if query and st.button("🔍 Run Graph Reasoning"):
            with st.spinner("Traversing knowledge web..."):
                result = engine.generate_verifiable_answer(query, model=model)
                
                # Display Trace
                with st.expander("🧠 View Reasoning Trace"):
                    for step in result.reasoning_trace:
                        st.markdown(f'<p class="reasoning-step">{step}</p>', unsafe_allow_html=True)
                
                # Display Answer
                st.markdown("### 💡 AI Intelligence Output")
                st.markdown(result.answer)
                
                # Display Citations
                if result.citations:
                    st.divider()
                    st.subheader("📚 Verified Citations")
                    for c in result.citations:
                        with st.expander(f"Reference {c.claim} - {c.source_document}"):
                            st.write(f"**Context Fragment:** {c.source_text}")

with tab_viz:
    st.subheader("📊 Research Graph Statistics")
    if st.button("Refresh Metrics"):
        # Real-time counts from Neo4j
        # (Simplified implementation)
        st.metric("Total Intelligence Nodes", "Scanning...")
        st.metric("Total Relationships", "Scanning...")
