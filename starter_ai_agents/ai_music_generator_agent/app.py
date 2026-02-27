import streamlit as st
import os
from datetime import datetime
from agents_config import get_music_composer_agent
from music_engine import MusicEngine
from utils import setup_logger, cleanup_generations

# Initialize logger
logger = setup_logger(__name__)

def init_app():
    """Setup page config and session state."""
    st.set_page_config(page_title="🎶 AI Music Studio", page_icon="🎶", layout="wide")
    
    if 'music_history' not in st.session_state:
        st.session_state.music_history = []
    if 'engine' not in st.session_state:
        st.session_state.engine = MusicEngine()

def main():
    init_app()
    
    with st.sidebar:
        st.title("🎶 Studio Config")
        st.markdown("---")
        
        # API Keys
        openai_key = st.text_input("OpenAI API Key", type="password")
        modelslab_key = st.text_input("ModelsLab API Key", type="password")
        
        st.markdown("---")
        if st.button("🗑️ Clear My Works"):
            cleanup_generations("audio_generations")
            st.session_state.music_history = []
            st.rerun()
            
        st.subheader("📜 Studio History")
        if st.session_state.music_history:
            for track in st.session_state.music_history:
                with st.expander(f"🎵 {track['time']} - {track['prompt'][:20]}..."):
                    st.audio(track['file'])
                    st.caption(track['prompt'])
        else:
            st.caption("No tracks generated yet.")

    st.title("🎶 AI Music Composition Studio")
    st.info("Your autonomous composer: Translating prompts into high-fidelity instrumental masterpieces.")

    # Main Input
    prompt = st.text_area("What kind of masterpiece should we compose today?", 
                         placeholder="e.g. A futuristic cyberpunk theme with heavy synths and dark atmospheric pads",
                         height=100)
    
    if st.button("🚀 Compose Track", type="primary", use_container_width=True):
        if not (openai_key and modelslab_key):
            st.error("Please provide both API keys in the sidebar.")
        elif not prompt.strip():
            st.warning("Please enter a composition prompt.")
        else:
            try:
                composer = get_music_composer_agent(openai_key, modelslab_key)
                
                with st.status("🎼 Orchestrating your track...", expanded=True) as status:
                    st.write("🤖 Strategizing musical elements...")
                    response = composer.run(prompt)
                    
                    if response.audio and len(response.audio) > 0:
                        st.write("📥 Downloading audio artifacts...")
                        url = response.audio[0].url
                        local_path = st.session_state.engine.download_audio(url)
                        
                        if local_path:
                            track_entry = {
                                "time": datetime.now().strftime("%H:%M:%S"),
                                "prompt": prompt,
                                "file": local_path
                            }
                            st.session_state.music_history.insert(0, track_entry)
                            st.session_state.active_track = track_entry
                            status.update(label="✅ Track Composed!", state="complete", expanded=False)
                        else:
                            st.error("Failed to download the generated audio.")
                    else:
                        st.error("AI failed to return audio content. Please check the prompt.")
                
            except Exception as e:
                st.error(f"Composition failed: {e}")
                logger.exception("Music Agent Error")

    # Active Result
    if hasattr(st.session_state, 'active_track'):
        track = st.session_state.active_track
        st.markdown("---")
        st.success(f"### Ready to Play: {track['prompt'][:50]}...")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.audio(track['file'])
        with col2:
            with open(track['file'], "rb") as f:
                st.download_button(
                    "📥 Download Master",
                    data=f.read(),
                    file_name=f"composition_{track['time'].replace(':', '')}.mp3",
                    mime="audio/mp3",
                    use_container_width=True
                )

if __name__ == "__main__":
    main()
