import os
import tempfile
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def process_pdf_fragment(file):
    """Cleanly extract and split PDF content into fragments."""
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
        tmp.write(file.getvalue())
        loader = PyPDFLoader(tmp.name)
        docs = loader.load()
        os.unlink(tmp.name)
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return splitter.split_documents(docs)

def init_routing_session():
    """Initialize multi-source session state."""
    defaults = {
        'openai_key': "",
        'qdrant_url': "",
        'qdrant_key': "",
        'ready': False
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def apply_routing_style():
    """Apply industrial data center aesthetics."""
    st.markdown("""
        <style>
        .stApp { background-color: #f8fafc; }
        .stSidebar { background-color: #1e293b !important; color: white; }
        .stTabs [aria-selected="true"] { border-bottom: 2px solid #3b82f6; }
        </style>
    """, unsafe_content_type=True)
import streamlit as st
