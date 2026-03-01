import streamlit as st
import asyncio
from datetime import datetime
from browser_engine import MemeGeneratorEngine
from utils import setup_logger

# Initialize logger
logger = setup_logger(__name__)

def init_session():
    """Initialize session state for history and settings."""
    if 'meme_history' not in st.session_state:
        st.session_state.meme_history = []
    if 'active_meme' not in st.session_state:
        st.session_state.active_meme = None

def main():
    st.set_page_config(page_title="🥸 AI Meme Hub", layout="wide", page_icon="🥸")
    init_session()

    # Custom CSS for high-end aesthetic
    st.markdown("""
        <style>
        .stButton>button {
            width: 100%;
            border-radius: 20px;
            height: 3em;
            background-color: #7B2CBF;
            color: white;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #9D4EDD;
            border-color: #7B2CBF;
        }
        .meme-card {
            border-radius: 15px;
            padding: 20px;
            background-color: #1a1c24;
            margin-bottom: 20px;
            border: 1px solid #3d4150;
        }
        </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.title("⚙️ Model Config")
        st.markdown("---")
        
        model_choice = st.selectbox(
            "Select Intelligence",
            ["Claude", "Deepseek", "OpenAI"],
            help="Choose the soul of your meme agent"
        )
        
        api_key = st.text_input(f"{model_choice} API Key", type="password")
        
        st.markdown("---")
        if st.button("🗑️ Clear My History"):
            st.session_state.meme_history = []
            st.session_state.active_meme = None
            st.rerun()

        st.subheader("📜 My Meme Gallery")
        if st.session_state.meme_history:
            for i, item in enumerate(st.session_state.meme_history):
                if st.button(f"🎭 {item['query'][:20]}...", key=f"hist_{i}"):
                    st.session_state.active_meme = item
        else:
            st.caption("No memes generated yet.")

    st.title("🥸 AI Meme Generator Agent")
    st.info("Direct browser automation for generating custom memes. The agent navigates ImgFlip to craft your perfect joke.")

    # Input Area
    query = st.text_input("What's the meme concept?", placeholder="e.g. Developer finally fixing a bug after 3 days")
    
    if st.button("🚀 Compose Meme via Browser", type="primary"):
        if not api_key:
            st.error(f"Please provide the {model_choice} API key in the sidebar.")
        elif not query:
            st.warning("Please describe your meme idea.")
        else:
            try:
                engine = MemeGeneratorEngine(model_choice, api_key)
                
                with st.status("🕵️ Browser Agent at Work...", expanded=True) as status:
                    st.write("🌍 Navigating to ImgFlip...")
                    # Note: streamlit runs in a sync context, we need to run the async engine
                    meme_url = asyncio.run(engine.generate_meme(query))
                    
                    if meme_url:
                        entry = {
                            "time": datetime.now().strftime("%H:%M:%S"),
                            "query": query,
                            "url": meme_url,
                            "model": model_choice
                        }
                        st.session_state.meme_history.insert(0, entry)
                        st.session_state.active_meme = entry
                        status.update(label="✅ Meme Crafted!", state="complete", expanded=False)
                    else:
                        st.error("Browser agent failed to capture the meme URL. Check logs.")
                
            except Exception as e:
                st.error(f"Generation failed: {e}")
                logger.exception("Meme Agent Runtime Error")

    # Display Active Result
    if st.session_state.active_meme:
        meme = st.session_state.active_meme
        st.markdown("---")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"### 🎨 {meme['query']}")
            st.image(meme['url'], use_container_width=True)
            
        with col2:
            st.markdown("### 🛠️ Options")
            st.markdown(f"**Model Used:** {meme['model']}")
            st.markdown(f"**Generated at:** {meme['time']}")
            
            st.markdown(f"[🔗 Open in High Quality]({meme['url']})")
            
            # Simple metadata copy helper
            st.code(meme['url'], language="text")
            st.caption("Direct Image Link")

if __name__ == "__main__":
    main()
