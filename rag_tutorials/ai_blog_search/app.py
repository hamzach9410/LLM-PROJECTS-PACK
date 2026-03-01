import streamlit as st
from langchain_core.messages import HumanMessage
from langchain.tools.retriever import create_retriever_tool
from rag_config import BlogSearchConfig
from vector_store import BlogVectorManager
from graph_logic import BlogGraphBuilder
from utils import init_blog_session, apply_blog_style

st.set_page_config(page_title="AI Research Hub", layout="wide")
apply_blog_style()
init_blog_session()

st.title("🔍 AI Strategic Blog Intelligence Hub")
st.markdown("---")

# Sidebar - Cluster Config
with st.sidebar:
    st.header("🔑 Intelligence Keys")
    g_key = st.text_input("Gemini API Key", type="password", value=st.session_state.gemini_key)
    q_host = st.text_input("Qdrant Host URL", value=st.session_state.qdrant_host)
    q_key = st.text_input("Qdrant API Key", type="password", value=st.session_state.qdrant_key)
    
    if st.button("🚀 Synchronize Cluster"):
        if all([g_key, q_host, q_key]):
            st.session_state.gemini_key = g_key
            st.session_state.qdrant_host = q_host
            st.session_state.qdrant_key = q_key
            st.success("Research Cluster Synced.")

# Infra Guard
if not all([st.session_state.gemini_key, st.session_state.qdrant_host, st.session_state.qdrant_key]):
    st.info("👋 Welcome! Please synchronize your research cluster in the sidebar to begin AI blog analysis.")
    st.stop()

# Initialize Engines
cfg = BlogSearchConfig(st.session_state.gemini_key, st.session_state.qdrant_host, st.session_state.qdrant_key)
vs = cfg.get_vector_store()
v_mgr = BlogVectorManager(vs)

# Ingestion
st.subheader("📥 Strategic Blog Ingestion")
blog_url = st.text_input("Blog Source URL (LLM, Prompt Eng, etc.)", placeholder="e.g., https://lilianweng.github.io/posts/2023-06-23-agent/")
if st.button("Index Source"):
    if blog_url:
        with st.spinner("Crawling and fragmenting intelligence data..."):
            count = v_mgr.ingest_blog(blog_url)
            st.session_state.ready = True
            st.success(f"Synchronized {count} research fragments.")

# Research Query
if st.session_state.ready:
    st.divider()
    query = st.text_area("Enter your research query:", placeholder="e.g., How does Lilian Weng compare ReAct to Chain of Thought?")
    
    if st.button("Execute Strategic Retrieval"):
        retriever_tool = create_retriever_tool(vs.as_retriever(), "blog_search", "Search AI blog intelligence.")
        builder = BlogGraphBuilder(cfg, vs.as_retriever())
        graph = builder.build_graph(retriever_tool)
        
        with st.spinner("Orchestrating self-correcting RAG loop..."):
            inputs = {"messages": [HumanMessage(content=query)]}
            res = graph.invoke(inputs)
            st.markdown("### 📊 Research Synthesis")
            st.write(res["messages"][-1].content)
else:
    st.info("Index an AI research blog to activate the intelligence hub.")