import os
import uuid
import asyncio
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv

from agents import Runner, trace
from agents_config import triage_agent, editor_agent, research_agent
from utils import setup_logger

# Load environment variables
load_dotenv()

# Initialize logger
logger = setup_logger(__name__)

def init_app():
    """Set up page configuration and session state."""
    st.set_page_config(
        page_title="Researcher Intelligence Dashboard",
        page_icon="📰",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    if "conversation_id" not in st.session_state:
        st.session_state.conversation_id = str(uuid.uuid4().hex[:16])
    if "collected_facts" not in st.session_state:
        st.session_state.collected_facts = []
    if "research_done" not in st.session_state:
        st.session_state.research_done = False
    if "report_result" not in st.session_state:
        st.session_state.report_result = None
    if "research_history" not in st.session_state:
        st.session_state.research_history = []
    if "current_agent" not in st.session_state:
        st.session_state.current_agent = "Idle"

async def run_research(topic):
    """Main research workflow refined for modular SDK code."""
    st.session_state.collected_facts = []
    st.session_state.research_done = False
    st.session_state.report_result = None
    st.session_state.current_agent = "Triage Agent (Planning)"
    
    with trace("News Research", group_id=st.session_state.conversation_id):
        # 1. Triage Phase
        triage_result = await Runner.run(
            triage_agent,
            f"Research this topic thoroughly: {topic}. This research will be used to create a comprehensive research report."
        )
        
        st.session_state.current_agent = "Research Agent (Collecting Facts)"
        # Note: Research Agent is called via handoff in the SDK workflow internally if instructions are followed, 
        # but the Runner handles the handoff logic.
        
        # 2. Wait for facts or progress
        await asyncio.sleep(2) 
        
        st.session_state.current_agent = "Editor Agent (Writing Report)"
        
        try:
            report_result = await Runner.run(
                editor_agent,
                triage_result.to_input_list()
            )
            
            st.session_state.report_result = report_result.final_output
            
            # Save to history (Contribution 13)
            st.session_state.research_history.append({
                "topic": topic,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "report": st.session_state.report_result
            })
            
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            st.error(f"Error generating report: {str(e)}")
    
    st.session_state.current_agent = "Idle"
    st.session_state.research_done = True

def main():
    init_app()
    
    if not os.environ.get("OPENAI_API_KEY"):
        st.error("Please set your OPENAI_API_KEY environment variable")
        st.stop()

    # Sidebar UI (Contribution 12, 13, 15)
    with st.sidebar:
        st.title("📰 Research Hub")
        user_topic = st.text_input("Enter Topic:", placeholder="Future of AI in Healthcare")
        
        col1, col2 = st.columns(2)
        start_btn = col1.button("🚀 Start", type="primary", use_container_width=True)
        if col2.button("🗑️ Clear", use_container_width=True):
            st.session_state.research_history = []
            st.session_state.research_done = False
            st.rerun()

        st.divider()
        st.subheader("📚 Research History")
        if st.session_state.research_history:
            for item in st.session_state.research_history:
                if st.button(f"📄 {item['topic']}", key=f"hist_{item['timestamp']}"):
                    st.session_state.report_result = item['report']
                    st.session_state.research_done = True
        else:
            st.caption("No history yet.")

    # Main Area
    st.title("📰 OpenAI Research Intelligence Platform")
    
    # Status Dashboard (Contribution 14)
    if st.session_state.current_agent != "Idle":
        st.info(f"🔄 **Current Status**: {st.session_state.current_agent}")
        st.progress(0.5 if "Research" in st.session_state.current_agent else 0.8 if "Editor" in st.session_state.current_agent else 0.2)
    
    tab1, tab2 = st.tabs(["🔍 Research Process", "📝 Final Report"])

    with tab1:
        if start_btn and user_topic:
            with st.spinner(f"Agent Team exploring: {user_topic}"):
                asyncio.run(run_research(user_topic))
        
        if st.session_state.collected_facts:
            st.markdown("### 📚 Knowledge Base (Facts Extracted)")
            for fact in st.session_state.collected_facts:
                st.success(f"**Fact**: {fact['fact']}\n\n*Source: {fact['source']}*")
        else:
            st.info("Start a research task to see facts appearing here in real-time.")

    with tab2:
        if st.session_state.research_done and st.session_state.report_result:
            report = st.session_state.report_result
            
            if hasattr(report, 'title'):
                st.header(report.title)
                
                with st.expander("📝 Report Outline"):
                    for i, o in enumerate(report.outline):
                        st.write(f"{i+1}. {o}")
                
                st.markdown(report.report)
                
                with st.expander("🔗 Sources"):
                    for s in report.sources:
                        st.write(f"- {s}")
                
                # Download Button (Contribution 17)
                st.download_button(
                    "📥 Download Research Report",
                    data=report.report,
                    file_name=f"{report.title.replace(' ', '_')}.md",
                    mime="text/markdown"
                )
            else:
                st.markdown(str(report))
        else:
            st.caption("The final report will be displayed here once generated.")

if __name__ == "__main__":
    main()
