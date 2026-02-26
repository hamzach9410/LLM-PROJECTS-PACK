import streamlit as st
import asyncio
import os
import json
from typing import List, Optional
from manager import TourManager
from agents import set_default_openai_key
from utils import generate_tts_audio, setup_logger
from config import VOICE_OPTIONS, INTEREST_OPTIONS, DEFAULT_VOICE, WORDS_PER_MINUTE

# Initialize logger
logger = setup_logger(__name__)

def init_session_state():
    """Initialize session state variables."""
    if "tour_history" not in st.session_state:
        st.session_state.tour_history = []
    if "OPENAI_API_KEY" not in st.session_state:
        st.session_state.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

def sidebar_setup():
    """Configure sidebar with settings."""
    with st.sidebar:
        st.title("⚙️ Settings")
        st.markdown("---")
        
        # API Key
        api_key_input = st.text_input("OpenAI API Key:", value=st.session_state.OPENAI_API_KEY, type="password")
        if api_key_input:
            st.session_state.OPENAI_API_KEY = api_key_input
            set_default_openai_key(api_key_input)
            os.environ["OPENAI_API_KEY"] = api_key_input

        st.markdown("---")
        st.markdown("### 🎙️ Narrator Settings")
        voice = st.selectbox("Select Guide Voice", options=VOICE_OPTIONS, index=VOICE_OPTIONS.index(DEFAULT_VOICE))
        speed = st.slider("Speech Speed", 0.5, 2.0, 1.0, step=0.1)
        
        st.markdown("---")
        if st.button("🗑️ Clear History"):
            st.session_state.tour_history = []
            st.rerun()
            
    return voice, speed

def main():
    st.set_page_config(page_title="AI Audio Tour Agent", page_icon="🎧", layout="wide")
    init_session_state()
    voice, speed = sidebar_setup()

    st.title("🎧 AI Audio Tour Agent")
    st.info("I'll help you explore any location with a personalized audio tour tailored to your interests.")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### 📍 Location")
        location = st.text_input("", placeholder="e.g., The Colosseum, Rome", label_visibility="collapsed")
        
        st.markdown("### 🎯 Interests")
        selected_interests = st.multiselect("", options=INTEREST_OPTIONS, default=["History", "Architecture"], label_visibility="collapsed")

    with col2:
        st.markdown("### ⏱️ Duration")
        duration_mins = st.slider("Tour Length (minutes)", 5, 60, 15, step=5)
        
        # Word count estimation
        est_words = duration_mins * WORDS_PER_MINUTE
        st.caption(f"Estimated length: ~{est_words} words")

    if st.button("🎧 Generate Personalized Tour", type="primary"):
        if not st.session_state.OPENAI_API_KEY:
            st.error("Please provide an OpenAI API Key in the sidebar.")
        elif not location:
            st.error("Please enter a location.")
        elif not selected_interests:
            st.warning("Please select at least one interest.")
        else:
            try:
                with st.status(f"Creating your tour of {location}...", expanded=True) as status:
                    st.write("🕵️ Researching landmarks and stories...")
                    mgr = TourManager()
                    # manager.run is async
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    tour_content = loop.run_until_complete(mgr.run(location, selected_interests, str(duration_mins)))
                    
                    st.write("🎙️ Generating high-quality audio narration...")
                    audio_path = generate_tts_audio(tour_content, voice=voice, speed=speed)
                    status.update(label="✅ Tour Ready!", state="complete")

                # Display Result
                st.markdown("---")
                st.markdown(f"## 🏛️ Your Tour of {location}")
                
                res_col1, res_col2 = st.columns([2, 1])
                with res_col1:
                    st.markdown("### 📝 Tour Transcript")
                    st.write(tour_content)
                
                with res_col2:
                    st.markdown("### 🔊 Audio Guide")
                    st.audio(str(audio_path))
                    
                    # Download Buttons
                    with open(audio_path, "rb") as f:
                        st.download_button("📥 Download MP3", data=f, file_name=f"{location.replace(' ','_')}_tour.mp3", mime="audio/mp3")
                    
                    st.download_button("📝 Download Transcript", data=tour_content, file_name=f"{location.replace(' ','_')}_transcript.txt")
                    
                    # Maps Link
                    maps_url = f"https://www.google.com/maps/search/?api=1&query={location.replace(' ','+')}"
                    st.link_button("📍 View on Google Maps", maps_url)

                st.session_state.tour_history.append({"location": location, "content": tour_content})

            except Exception as e:
                st.error(f"Failed to generate tour: {e}")
                logger.exception("Tour generation error")

    if st.session_state.tour_history:
        st.markdown("---")
        st.markdown("### 📜 Recent Tours")
        for h in reversed(st.session_state.tour_history):
            with st.expander(f"📍 {h['location']}"):
                st.write(h['content'])

if __name__ == "__main__":
    main()
