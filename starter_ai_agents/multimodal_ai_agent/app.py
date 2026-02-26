import streamlit as st
import os
import pandas as pd
from datetime import datetime
from agents_config import get_multimodal_agent
from media_processor import MediaProcessor
from utils import setup_logger, cleanup_temp_file

# Initialize logger
logger = setup_logger(__name__)

def init_session():
    """Initialize session state for history and keys."""
    if 'analysis_history' not in st.session_state:
        st.session_state.analysis_history = []
    if 'gemini_api_key' not in st.session_state:
        st.session_state.gemini_api_key = os.getenv("GEMINI_API_KEY", "")

def main():
    st.set_page_config(page_title="🧬 Multimodal AI Hub", layout="wide", page_icon="🧬")
    init_session()

    with st.sidebar:
        st.title("🧬 Configuration")
        st.markdown("---")
        
        # API Key management
        api_key = st.text_input("Gemini API Key", value=st.session_state.gemini_api_key, type="password")
        if api_key:
            st.session_state.gemini_api_key = api_key
            os.environ["GEMINI_API_KEY"] = api_key

        # Model selection
        model_choice = st.selectbox("Intelligence Level", ["gemini-2.0-flash", "gemini-1.5-pro"], index=0)
        
        st.markdown("---")
        if st.button("🗑️ Clear All History"):
            st.session_state.analysis_history = []
            st.rerun()

        st.subheader("📚 Analysis History")
        if st.session_state.analysis_history:
            for item in st.session_state.analysis_history:
                if st.button(f"📄 {item['filename']} ({item['timestamp']})", key=f"hist_{item['timestamp']}"):
                    st.session_state.selected_analysis = item
        else:
            st.caption("No history yet.")

    st.title("🧬 Multimodal Intelligence Dashboard")
    st.info("Upload Images, Videos, or PDFs for deep cross-media analysis and reasoning.")

    # Main Interaction Area
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### 📤 Upload Media")
        uploaded_file = st.file_uploader("Drop image, video, or PDF", type=['png', 'jpg', 'jpeg', 'mp4', 'mov', 'avi', 'pdf'])
        
        if uploaded_file:
            st.markdown("### 👀 Preview")
            if uploaded_file.type.startswith('image'):
                st.image(uploaded_file, use_container_width=True)
            elif uploaded_file.type.startswith('video'):
                st.video(uploaded_file)
            elif uploaded_file.type == 'application/pdf':
                st.caption(f"PDF Document: {uploaded_file.name}")

    with col2:
        st.markdown("### ✨ Reasoning Task")
        user_prompt = st.text_area("What should the agent look for?", placeholder="Summarize this video and extract key features...", height=150)
        
        if st.button("🚀 Run Multimodal Analysis", type="primary", use_container_width=True):
            if not st.session_state.gemini_api_key:
                st.error("Please provide a Gemini API Key in the sidebar.")
            elif not uploaded_file:
                st.warning("Please upload a file first.")
            elif not user_prompt:
                st.warning("Please enter your query prompt.")
            else:
                try:
                    with st.spinner(f"Agent is analyzing {uploaded_file.name}..."):
                        temp_path, f_type = MediaProcessor.process_upload(uploaded_file)
                        media_obj = MediaProcessor.get_agno_media(temp_path, f_type)
                        
                        agent = get_multimodal_agent(st.session_state.gemini_api_key, model_id=model_choice)
                        
                        # Prepare run arguments
                        kwargs = {}
                        if f_type in ['png', 'jpg', 'jpeg']:
                            kwargs['images'] = [media_obj]
                        elif f_type in ['mp4', 'mov', 'avi']:
                            kwargs['videos'] = [media_obj]
                        elif f_type == 'pdf':
                            kwargs['documents'] = [media_obj]

                        result = agent.run(user_prompt, **kwargs)
                        
                        # Store in history
                        st.session_state.analysis_history.append({
                            "filename": uploaded_file.name,
                            "timestamp": datetime.now().strftime("%H:%M:%S"),
                            "content": result.content,
                            "prompt": user_prompt
                        })
                        
                        st.success("Analysis Complete!")
                        st.markdown(result.content)
                        
                        # Cleanup
                        cleanup_temp_file(temp_path)
                        
                        # Export Button (Contribution 17)
                        st.download_button("📥 Export Report (Markdown)", data=result.content, file_name=f"{uploaded_file.name}_analysis.md")

                except Exception as e:
                    st.error(f"Analysis failed: {e}")
                    logger.exception("Media run error")

if __name__ == "__main__":
    main()
