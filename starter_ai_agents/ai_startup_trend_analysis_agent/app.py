import streamlit as st
import asyncio
import os
from datetime import datetime
from analysis_engine import AnalysisEngine
from utils import setup_logger, format_analysis_report

# Initialize logger
logger = setup_logger(__name__)

def init_session():
    """Setup session state for history and API keys."""
    if 'analysis_history' not in st.session_state:
        st.session_state.analysis_history = []
    if 'gemini_api_key' not in st.session_state:
        st.session_state.gemini_api_key = os.getenv("GOOGLE_API_KEY", "")

def main():
    st.set_page_config(page_title="📈 Startup Intelligence Hub", layout="wide", page_icon="📈")
    init_session()

    with st.sidebar:
        st.title("📈 Strategic Config")
        st.markdown("---")
        
        api_key = st.text_input("Gemini (Google) API Key", value=st.session_state.gemini_api_key, type="password")
        if api_key:
            st.session_state.gemini_api_key = api_key
            os.environ["GOOGLE_API_KEY"] = api_key

        model_choice = st.selectbox("Intelligence Level", ["gemini-2.0-flash", "gemini-1.5-pro"])
        
        st.markdown("---")
        if st.button("🗑️ Clear History"):
            st.session_state.analysis_history = []
            st.rerun()

        st.subheader("📜 Recent Reports")
        if st.session_state.analysis_history:
            for report in st.session_state.analysis_history:
                if st.button(f"📊 {report['topic']} ({report['time']})", key=f"hist_{report['time']}"):
                    st.session_state.active_report = report
        else:
            st.caption("No reports in history yet.")

    st.title("📈 AI Startup Trend Analysis Platform")
    st.info("Direct from market signals to strategic startup opportunities using Multi-Agent Intelligence.")

    # Input Area
    topic = st.text_input("What industry or niche are you exploring?", placeholder="e.g. AI-driven cybersecurity for SMEs")
    
    if st.button("🚀 Generate Strategic Analysis", type="primary", use_container_width=True):
        if not st.session_state.gemini_api_key:
            st.error("Please provide an API Key in the sidebar.")
        elif not topic:
            st.warning("Please enter a topic.")
        else:
            try:
                engine = AnalysisEngine(st.session_state.gemini_api_key, model_choice)
                
                with st.status("🛠️ Startup Strategists at Work...", expanded=True) as status:
                    progress_text = st.empty()
                    
                    # Run logic
                    result = asyncio.run(engine.run_analysis(topic, progress_callback=lambda t: progress_text.write(t)))
                    
                    # Post-process
                    final_report = format_analysis_report(result['analysis'])
                    
                    # Update History
                    report_entry = {
                        "topic": topic,
                        "time": datetime.now().strftime("%H:%M:%S"),
                        "report": final_report,
                        "summaries": result['summaries']
                    }
                    st.session_state.analysis_history.append(report_entry)
                    st.session_state.active_report = report_entry
                    
                    status.update(label="✅ Strategy Report Generated!", state="complete", expanded=False)
                
            except Exception as e:
                st.error(f"Analysis failed: {e}")
                logger.exception("Engine Run Error")

    # Main Output Display
    if hasattr(st.session_state, 'active_report'):
        report = st.session_state.active_report
        st.markdown("---")
        
        tab1, tab2 = st.tabs(["📊 Strategic Analysis", "📝 Industry Summaries"])
        
        with tab1:
            st.markdown(report['report'])
            # Export (Contribution 17)
            st.download_button("📥 Download Trend Report (Markdown)", data=report['report'], file_name=f"{report['topic'].replace(' ', '_')}_trends.md")

        with tab2:
            st.markdown(report['summaries'])

if __name__ == "__main__":
    main()
