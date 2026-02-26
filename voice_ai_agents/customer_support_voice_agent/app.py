import streamlit as st
import asyncio
import os
import tempfile
import uuid
import logging
import json
from typing import Dict, Optional
from openai import AsyncOpenAI
from agents import Runner

from crawler_engine import CrawlerRAGEngine
from agents_config import setup_agents
from utils import setup_logger

# Initialize logger
logger = setup_logger(__name__)

def init_session_state() -> None:
    """Initialize Streamlit session state."""
    defaults = {
        "qdrant_url": "",
        "qdrant_api_key": "",
        "firecrawl_api_key": "",
        "openai_api_key": "",
        "doc_url": "",
        "setup_complete": False,
        "engine": None,
        "processor_agent": None,
        "tts_agent": None,
        "selected_voice": "coral",
        "chat_history": [],
        "crawl_limit": 5,
        "voice_speed": 1.0
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def setup_sidebar() -> None:
    """Configure sidebar with settings and controls."""
    with st.sidebar:
        st.title("🎙️ Agent Config")
        st.markdown("---")
        
        with st.expander("🔑 API Credentials", expanded=not st.session_state.setup_complete):
            st.session_state.qdrant_url = st.text_input("Qdrant URL", value=st.session_state.qdrant_url, type="password")
            st.session_state.qdrant_api_key = st.text_input("Qdrant API Key", value=st.session_state.qdrant_api_key, type="password")
            st.session_state.firecrawl_api_key = st.text_input("Firecrawl API Key", value=st.session_state.firecrawl_api_key, type="password")
            st.session_state.openai_api_key = st.text_input("OpenAI API Key", value=st.session_state.openai_api_key, type="password")
        
        st.session_state.doc_url = st.text_input("Documentation URL", value=st.session_state.doc_url, placeholder="https://docs.openai.com")
        st.session_state.crawl_limit = st.slider("Crawl Page Limit", 1, 20, 5)
        
        st.markdown("---")
        st.markdown("### 🎤 Voice Settings")
        voices = ["alloy", "ash", "ballad", "coral", "echo", "fable", "onyx", "nova", "sage", "shimmer", "verse"]
        st.session_state.selected_voice = st.selectbox("Select Voice", options=voices, index=voices.index(st.session_state.selected_voice))
        st.session_state.voice_speed = st.slider("Speech Speed", 0.5, 2.0, 1.0)
        
        if st.button("🚀 Initialize/Reset System", type="primary"):
            if all([st.session_state.qdrant_url, st.session_state.qdrant_api_key, 
                    st.session_state.firecrawl_api_key, st.session_state.openai_api_key, st.session_state.doc_url]):
                try:
                    with st.spinner("🔄 Crawling and indexing documentation..."):
                        engine = CrawlerRAGEngine(st.session_state.qdrant_url, st.session_state.qdrant_api_key)
                        engine.reset() # Clear previous crawl
                        pages = engine.crawl_docs(st.session_state.firecrawl_api_key, st.session_state.doc_url, st.session_state.crawl_limit)
                        engine.store_embeddings(pages)
                        
                        p, t = setup_agents(st.session_state.openai_api_key)
                        st.session_state.engine = engine
                        st.session_state.processor_agent = p
                        st.session_state.tts_agent = t
                        st.session_state.setup_complete = True
                        st.success(f"Successfully indexed {len(pages)} pages!")
                except Exception as e:
                    st.error(f"Initialization failed: {e}")
            else:
                st.warning("Please fill in all credentials and the URL.")

        if st.session_state.chat_history:
            st.markdown("---")
            chat_json = json.dumps(st.session_state.chat_history, indent=2)
            st.download_button("📥 Download Transcript", data=chat_json, file_name="support_transcript.json", mime="application/json")

async def process_query_handler(query: str) -> Optional[Dict]:
    """Process user query and generate voice response."""
    try:
        # Search
        search_results = st.session_state.engine.search(query)
        if not search_results:
            st.warning("No relevant info found.")
            return None
        
        # Context
        context = "Based on the following documentation:\n\n"
        source_links = []
        for result in search_results:
            payload = result.payload
            url = payload.get('url', 'Unknown URL')
            content = payload.get('content', '')
            context += f"From {url}:\n{content}\n\n"
            source_links.append(url)
        
        context += f"\nUser Question: {query}\n"
        
        # Step 3: Agents
        with st.spinner("🧠 Analyzing docs..."):
            p_res = await Runner.run(st.session_state.processor_agent, context)
            text_response = p_res.final_output
        
        with st.spinner("🎨 Formatting speech..."):
            t_res = await Runner.run(st.session_state.tts_agent, text_response)
            voice_instructions = t_res.final_output
        
        # Step 4: Audio
        async_openai = AsyncOpenAI(api_key=st.session_state.openai_api_key)
        audio_res = await async_openai.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice=st.session_state.selected_voice,
            input=text_response,
            instructions=voice_instructions,
            response_format="mp3",
            speed=st.session_state.voice_speed
        )
        
        temp_path = os.path.join(tempfile.gettempdir(), f"support_res_{uuid.uuid4()}.mp3")
        with open(temp_path, "wb") as f:
            f.write(audio_res.content)
            
        return {
            "text": text_response,
            "audio": temp_path,
            "sources": list(set(source_links))
        }
    except Exception as e:
        st.error(f"Error: {e}")
        return None

def main():
    st.set_page_config(page_title="Support Voice Agent", page_icon="🎙️", layout="wide")
    init_session_state()
    setup_sidebar()
    
    st.title("🎙️ Customer Support Voice Agent")
    st.markdown("### Instantly answer customer questions with voice narration")
    
    query = st.text_input("Enter your question about the documentation:", disabled=not st.session_state.setup_complete)
    
    if query:
        res = asyncio.run(process_query_handler(query))
        if res:
            st.markdown("---")
            col_a, col_b = st.columns([2, 1])
            with col_a:
                st.markdown("#### 💬 Agent Response")
                st.write(res["text"])
            with col_b:
                st.markdown("#### 🔊 Voice Playback")
                st.audio(res["audio"])
            
            with st.expander("🔗 Reference Sources"):
                for s in res["sources"]:
                    st.markdown(f"- [{s}]({s})")
            
            st.session_state.chat_history.append({"q": query, "a": res["text"]})

    if st.session_state.chat_history:
        st.markdown("---")
        st.markdown("### 📜 Session History")
        for item in reversed(st.session_state.chat_history):
            with st.chat_message("user"):
                st.write(item["q"])
            with st.chat_message("assistant"):
                st.write(item["a"])

if __name__ == "__main__":
    main()
