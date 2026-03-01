import streamlit as st
import numpy as np
import os
from agents_config import VisionConfig
from rag_engine import VisionRAGEngine
from utils import init_vision_session, apply_vision_style, pil_to_base64_data

st.set_page_config(page_title="Vision Creative Studio", layout="wide")
apply_vision_style()
init_vision_session()

st.title("🎨 Vision Multimodal Research Studio")
st.markdown("---")

# Sidebar - API Cluster
with st.sidebar:
    st.header("🔑 Vision Infrastructure")
    c_key = st.text_input("Cohere API Key", type="password", value=st.session_state.cohere_key)
    g_key = st.text_input("Google API Key", type="password", value=st.session_state.google_key)
    
    if st.button("🚀 Initialize Vision Core", use_container_width=True):
        if c_key and g_key:
            st.session_state.cohere_key = c_key
            st.session_state.google_key = g_key
            st.success("Vision Core Initialized.")

# Check Infrastructure
if not st.session_state.cohere_key or not st.session_state.google_key:
    st.info("👋 Welcome! Please provide your Cohere and Google API keys in the sidebar to start multimodal research.")
    st.stop()

# Initialize Engine
cfg = VisionConfig(st.session_state.cohere_key, st.session_state.google_key)
engine = VisionRAGEngine(cfg.get_cohere_client(), cfg.get_gemini_client())

# Multi-Source Ingestion
st.subheader("📥 Multimodal Knowledge Ingestion")
files = st.file_uploader("Upload Images (Infographics, Charts) or PDFs", type=['png', 'jpg', 'jpeg', 'pdf'], accept_multiple_files=True)

if files:
    if st.button("🚀 Process Intelligence fragments"):
        new_paths, new_embs = [], []
        for f in files:
            with st.spinner(f"Ingesting {f.name}..."):
                if f.type == "application/pdf":
                    p, e = engine.process_pdf(f)
                    new_paths.extend(p)
                    new_embs.extend(e)
                else:
                    import PIL.Image
                    img = PIL.Image.open(f)
                    path = f"vault_{f.name}"
                    img.save(path)
                    emb = engine.embed_multimodal(pil_to_base64_data(img))
                    new_paths.append(path)
                    new_embs.append(emb)
        
        if new_paths:
            st.session_state.image_paths.extend(new_paths)
            st.session_state.doc_embeddings = np.vstack(new_embs) if st.session_state.doc_embeddings is None else np.vstack((st.session_state.doc_embeddings, new_embs))
            st.success(f"Synchronized {len(new_paths)} visual fragments.")

# Visual Research
if st.session_state.image_paths:
    st.divider()
    query = st.text_input("Ask a question about your visual knowledge (Charts, Graphs, etc.):", placeholder="e.g., What is the quarterly growth shown in the diagram?")
    
    if st.button("🔍 Execute Cross-Modal Search"):
        if query:
            with st.spinner("Executing cross-modal search..."):
                hit_path = engine.search_intelligence(query, st.session_state.doc_embeddings, st.session_state.image_paths)
                st.image(hit_path, caption=f"Retrieved Source: {os.path.basename(hit_path)}", use_container_width=True)
                
                with st.spinner("Synthesizing answer from visual context..."):
                    ans = engine.synthesize_answer(query, hit_path)
                    st.markdown("### 📊 Visual Synthesis Result")
                    st.write(ans)
else:
    st.info("Ingest visual sources to activate the research studio.")
