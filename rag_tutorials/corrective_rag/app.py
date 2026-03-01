import streamlit as st
import os
import pprint
from llm_config import LLMConfig
from vector_store import VectorStoreManager
from rag_logic import RAGLogic
from graph_config import CorrectiveGraph

st.set_page_config(page_title="Corrective RAG Orchestrator", layout="wide")

st.title("🔄 Corrective RAG Intelligence Studio")
st.markdown("---")

# Configuration
with st.sidebar:
    st.header("🔑 API Configuration")
    openai_key = st.text_input("OpenAI API Key", type="password", value=os.getenv("OPENAI_API_KEY", ""))
    anthropic_key = st.text_input("Anthropic API Key", type="password", value=os.getenv("ANTHROPIC_API_KEY", ""))
    tavily_key = st.text_input("Tavily API Key", type="password", value=os.getenv("TAVILY_API_KEY", ""))
    qdrant_url = st.text_input("Qdrant URL", value="http://localhost:6333")
    qdrant_key = st.text_input("Qdrant API Key", type="password")

if not all([openai_key, anthropic_key, tavily_key]):
    st.info("👋 Please configure your API keys in the sidebar to activate the Corrective RAG Agent.")
    st.stop()

# Initialize Managers
llm_manager = LLMConfig(openai_key, anthropic_key)
vstore_manager = VectorStoreManager(qdrant_url, qdrant_key, llm_manager.get_embeddings())

# Document Ingest
st.subheader("📚 Knowledge Ingestion")
col1, col2 = st.columns(2)
with col1:
    input_type = st.radio("Source Type", ["URL", "File"])
with col2:
    if input_type == "URL":
        source = st.text_input("Enter Document URL", value="https://arxiv.org/pdf/2307.09288.pdf")
    else:
        source_file = st.file_uploader("Upload Document", type=["pdf", "txt"])
        source = source_file.name if source_file else None

if st.button("🚀 Process & Index Documents", type="primary"):
    with st.spinner("📦 Indexing to Qdrant..."):
        # Document loading logic
        if input_type == "URL":
            docs = RAGLogic.load_document(source, is_url=True)
        else:
            # Handle local file upload (placeholder for actual read)
            docs = [] # Simplified for now
            
        if docs:
            from langchain.text_splitter import RecursiveCharacterTextSplitter
            splits = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100).split_documents(docs)
            vstore_manager.setup_collection()
            retriever = vstore_manager.add_documents(splits)
            st.session_state.retriever = retriever
            st.success("Indexing Complete!")

# Query Interface
if "retriever" in st.session_state:
    st.divider()
    query = st.text_input("📝 Ask a question about the indexed knowledge:")
    if st.button("🔍 Run Corrective Search"):
        graph = CorrectiveGraph(llm_manager, st.session_state.retriever, tavily_key)
        workflow = graph.compile_workflow()
        
        inputs = {"keys": {"question": query}}
        
        with st.status("🏗️ Orchestrating RAG Workflow...", expanded=True) as status:
            for output in workflow.stream(inputs):
                for key, value in output.items():
                    st.write(f"✅ Completed Step: **{key}**")
            status.update(label="Synthesis Complete!", state="complete")
            
            final_gen = list(output.values())[0]["keys"]["generation"]
            st.markdown("### 💡 AI Intelligence Output")
            st.markdown(final_gen)
