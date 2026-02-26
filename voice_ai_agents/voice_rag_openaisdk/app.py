import streamlit as st
import asyncio
import os
import tempfile
import uuid
import logging
import json
from typing import Dict, List, Optional
from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer
from agents import Runner

from rag_engine import RAGEngine
from agents_config import setup_agents
from utils import process_pdf

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def init_session_state() -> None:
    """Initialize Streamlit session state with default values."""
    defaults = {
        "qdrant_url": "",
        "qdrant_api_key": "",
        "openai_api_key": "",
        "setup_complete": False,
        "rag_engine": None,
        "processor_agent": None,
        "tts_agent": None,
        "selected_voice": "coral",
        "processed_documents": [],
        "chat_history": [],
        "chunk_size": 1000,
        "chunk_overlap": 200,
        "voice_speed": 1.0
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def setup_sidebar() -> None:
    """Configure sidebar with branding and settings."""
    with st.sidebar:
        st.image("https://skillicons.dev/icons?i=py,streamlit,openai", width=150)
        st.title("🎙️ Voice RAG Command")
        st.markdown("---")
        
        with st.expander("🔑 API Credentials", expanded=not st.session_state.setup_complete):
            st.session_state.qdrant_url = st.text_input("Qdrant URL", value=st.session_state.qdrant_url, type="password")
            st.session_state.qdrant_api_key = st.text_input("Qdrant API Key", value=st.session_state.qdrant_api_key, type="password")
            st.session_state.openai_api_key = st.text_input("OpenAI API Key", value=st.session_state.openai_api_key, type="password")
        
        with st.expander("⚙️ RAG Settings"):
            st.session_state.chunk_size = st.slider("Chunk Size", 500, 2000, 1000)
            st.session_state.chunk_overlap = st.slider("Overlap", 0, 500, 200)
            
        with st.expander("🎤 Voice Settings"):
            voices = ["alloy", "ash", "ballad", "coral", "echo", "fable", "onyx", "nova", "sage", "shimmer", "verse"]
            st.session_state.selected_voice = st.selectbox("Select Voice", options=voices, index=voices.index(st.session_state.selected_voice))
            st.session_state.voice_speed = st.slider("Speech Speed", 0.5, 2.0, 1.0)
        
        st.markdown("---")
        if st.button("🗑️ Reset All Data", help="Clear vector database and chat history"):
            if st.session_state.rag_engine:
                st.session_state.rag_engine.clear_collection()
            st.session_state.processed_documents = []
            st.session_state.chat_history = []
            st.success("System reset successfully!")
            st.rerun()
            
        if st.session_state.chat_history:
            chat_json = json.dumps(st.session_state.chat_history, indent=2)
            st.download_button(
                label="📥 Download Transcript",
                data=chat_json,
                file_name="voice_rag_transcript.json",
                mime="application/json"
            )

async def process_query_handler(query: str) -> Optional[Dict]:
    """Handle the end-to-end query processing with UI updates."""
    try:
        # 1. Search
        search_results = st.session_state.rag_engine.query(query)
        if not search_results:
            st.warning("No relevant information found in the documents.")
            return None
        
        # 2. Context Preparation
        context = "Based on the following documentation:\n\n"
        source_details = []
        for result in search_results:
            payload = result.payload
            content = payload.get('content', '')
            fname = payload.get('file_name', 'Unknown')
            context += f"From {fname}:\n{content}\n\n"
            source_details.append({"file": fname, "content": content})
        
        context += f"\nUser Question: {query}\n"
        
        # 3. Agent Execution
        if not st.session_state.processor_agent:
            p, t = setup_agents(st.session_state.openai_api_key)
            st.session_state.processor_agent, st.session_state.tts_agent = p, t
        
        with st.spinner("🧠 Thinking..."):
            p_res = await Runner.run(st.session_state.processor_agent, context)
            text_response = p_res.final_output
        
        with st.spinner("🎨 Refining speech..."):
            t_res = await Runner.run(st.session_state.tts_agent, text_response)
            voice_instructions = t_res.final_output
        
        # 4. Audio Generation
        async_openai = AsyncOpenAI(api_key=st.session_state.openai_api_key)
        
        # Try local playback via Runner helper if applicable, or standard API
        try:
            async with async_openai.audio.speech.with_streaming_response.create(
                model="gpt-4o-mini-tts",
                voice=st.session_state.selected_voice,
                input=text_response,
                instructions=voice_instructions,
                response_format="pcm",
                speed=st.session_state.voice_speed
            ) as stream:
                await LocalAudioPlayer().play(stream)
        except Exception as e:
            logger.warning(f"Local audio playback failed: {e}")

        # MP3 generation for Streamlit UI
        audio_res = await async_openai.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice=st.session_state.selected_voice,
            input=text_response,
            instructions=voice_instructions,
            response_format="mp3",
            speed=st.session_state.voice_speed
        )
        
        temp_path = os.path.join(tempfile.gettempdir(), f"res_{uuid.uuid4()}.mp3")
        with open(temp_path, "wb") as f:
            f.write(audio_res.content)
            
        return {
            "text": text_response,
            "audio": temp_path,
            "sources": source_details
        }
    except Exception as e:
        st.error(f"Failed to process query: {e}")
        logger.error(f"Query error: {e}", exc_info=True)
        return None

def main():
    st.set_page_config(page_title="Voice RAG Agent", page_icon="🎙️", layout="wide")
    init_session_state()
    setup_sidebar()
    
    st.title("🎙️ Voice RAG Agent")
    st.markdown("### Powerful RAG with real-time voice narration")
    
    # Grid layout for Upload and Stats
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_files = st.file_uploader(
            "Upload PDF Documents", 
            type=["pdf"], 
            accept_multiple_files=True,
            help="Select one or more PDFs to index for retrieval"
        )
    
    with col2:
        st.info(f"📚 Documents Indexed: {len(st.session_state.processed_documents)}")
        if st.session_state.processed_documents:
            with st.expander("View Document List"):
                for doc in st.session_state.processed_documents:
                    st.text(f"• {doc}")

    if uploaded_files:
        if not st.session_state.rag_engine:
            if all([st.session_state.qdrant_url, st.session_state.qdrant_api_key]):
                with st.spinner("Initializing Vector Engine..."):
                    st.session_state.rag_engine = RAGEngine(st.session_state.qdrant_url, st.session_state.qdrant_api_key)
            else:
                st.warning("Please provide Qdrant credentials in the sidebar.")
                return

        for f in uploaded_files:
            if f.name not in st.session_state.processed_documents:
                with st.spinner(f"Indexing {f.name}..."):
                    docs = process_pdf(f, st.session_state.chunk_size, st.session_state.chunk_overlap)
                    if docs:
                        st.session_state.rag_engine.store_documents(docs)
                        st.session_state.processed_documents.append(f.name)
                        st.toast(f"✅ Indexed {f.name}", icon='📄')
        st.session_state.setup_complete = True

    # Interaction Area
    query = st.text_input(
        "Ask a question:", 
        placeholder="e.g., What are the key takeaways from the uploaded files?",
        disabled=not st.session_state.setup_complete
    )
    
    if query:
        res = asyncio.run(process_query_handler(query))
        if res:
            st.markdown("---")
            st.markdown("#### 💬 Response")
            st.write(res["text"])
            st.audio(res["audio"])
            
            with st.expander("🔍 Source Preview"):
                for idx, src in enumerate(res["sources"]):
                    st.markdown(f"**Source {idx+1}: {src['file']}**")
                    st.caption(src["content"])
                    st.markdown("---")
            
            st.session_state.chat_history.append({
                "query": query, 
                "answer": res["text"],
                "timestamp": uuid.uuid4().hex[:8]
            })

    # History Section
    if st.session_state.chat_history:
        st.markdown("### 📜 Session History")
        for item in reversed(st.session_state.chat_history):
            with st.chat_message("user"):
                st.write(item["query"])
            with st.chat_message("assistant"):
                st.write(item["answer"])

if __name__ == "__main__":
    main()
