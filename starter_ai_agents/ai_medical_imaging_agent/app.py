import streamlit as st
import os
from PIL import Image as PILImage
from datetime import datetime
from agents_config import get_medical_agent
from imaging_engine import ImagingEngine
from utils import setup_logger, resize_medical_image, save_temp_image, cleanup_temp_files

# Initialize logger
logger = setup_logger(__name__)

def init_app():
    """Setup page config and session state."""
    st.set_page_config(page_title="🏥 Radiological Intelligence Hub", page_icon="🏥", layout="wide")
    
    if 'analysis_history' not in st.session_state:
        st.session_state.analysis_history = []
    if 'google_api_key' not in st.session_state:
        st.session_state.google_api_key = os.getenv("GOOGLE_API_KEY", "")

def main():
    init_app()
    
    with st.sidebar:
        st.title("🏥 Studio Config")
        st.markdown("---")
        
        # API Keys
        api_key = st.text_input("Google API Key", value=st.session_state.google_api_key, type="password")
        if api_key:
            st.session_state.google_api_key = api_key
            
        model_id = st.selectbox("Vision Model", ["gemini-2.0-flash-exp", "gemini-1.5-pro"])
        
        st.markdown("---")
        st.info("⚠ Disclaimer: For educational use only. consult a physician for medical advice.")
        
        if st.button("🗑️ Clear History"):
            st.session_state.analysis_history = []
            st.rerun()
            
        st.subheader("📜 Analysis History")
        if st.session_state.analysis_history:
            for entry in st.session_state.analysis_history:
                with st.expander(f"📍 {entry['time']} - {entry['diagnosis'][:20]}..."):
                    st.write(entry['diagnosis'])
        else:
            st.caption("No history yet.")

    st.title("🏥 Radiological AI Platform")
    st.write("Professional-grade diagnostic assistance using Gemini Vision.")

    if not st.session_state.google_api_key:
        st.warning("Please provide a Google API Key in the sidebar to begin.")
        st.stop()

    # File Uploader
    uploaded_file = st.file_uploader("Upload Medical Image (X-ray, MRI, CT, etc.)", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            raw_image = PILImage.open(uploaded_file)
            display_image = resize_medical_image(raw_image)
            st.image(display_image, caption="Uploaded Specimen", use_container_width=True)
            
            analyze_btn = st.button("🔍 Run Full Diagnostic Analysis", type="primary", use_container_width=True)
            
        with col2:
            if analyze_btn:
                try:
                    engine = ImagingEngine(st.session_state.google_api_key, model_id)
                    temp_path = "active_analysis.png"
                    save_temp_image(display_image, temp_path)
                    
                    with st.status("🏥 Diagnostic Pipeline Active...", expanded=True) as status:
                        st.write("👁️ Extracting visual features...")
                        analysis_text = engine.analyze_image(temp_path)
                        
                        entry = {
                            "time": datetime.now().strftime("%H:%M:%S"),
                            "diagnosis": analysis_text
                        }
                        st.session_state.analysis_history.insert(0, entry)
                        st.session_state.active_report = entry
                        
                        status.update(label="✅ Analysis Complete!", state="complete", expanded=False)
                    
                    cleanup_temp_files([temp_path])
                except Exception as e:
                    st.error(f"Analysis failed: {e}")
                    logger.exception("Engine Error")

    # Display Result
    if hasattr(st.session_state, 'active_report'):
        report = st.session_state.active_report
        st.markdown("---")
        st.subheader(f"📋 Diagnostic Report")
        
        tabs = st.tabs(["Analysis", "Raw Export"])
        with tabs[0]:
            st.markdown(report['diagnosis'])
        with tabs[1]:
            st.code(report['diagnosis'], language="markdown")
            st.download_button(
                "📥 Download Markdown Report",
                data=report['diagnosis'],
                file_name=f"report_{report['time'].replace(':', '')}.md",
                mime="text/markdown"
            )

if __name__ == "__main__":
    main()
