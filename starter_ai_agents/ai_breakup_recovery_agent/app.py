import streamlit as st
import os
from agents_config import get_recovery_agents
from recovery_engine import RecoveryEngine

# Page configuration
st.set_page_config(
    page_title="Breakup Recovery Hub",
    page_icon="❤️",
    layout="wide"
)

st.title("❤️ Relationship Wellness Platform")
st.markdown("---")

# Sidebar - Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    gemini_key = st.text_input("Gemini API Key", type="password", help="Enter your Google Gemini API Key")
    
    st.divider()
    st.markdown("""
    ### 🛡️ Your Privacy:
    This tool is designed for private reflection. No data is stored beyond this session.
    """)

if not gemini_key:
    st.info("💡 Please enter your Gemini API Key in the sidebar to begin.")
    st.stop()

os.environ["GOOGLE_API_KEY"] = gemini_key

# Initialize Engine and Agents
engine = RecoveryEngine()
counselor, strategist = get_recovery_agents()

# Main Interface
st.subheader("How are you feeling today?")
user_input = st.text_area("Share your thoughts/feelings...", placeholder="I've been feeling really overwhelmed lately...")

if st.button("🌱 Get Support"):
    if user_input:
        try:
            with st.spinner("💭 Thinking with compassion..."):
                empathy_resp, wellness_resp = engine.process_emotional_state(counselor, strategist, user_input)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.info("🧬 **Empathetic Guidance**")
                st.markdown(empathy_resp.content)
            
            with col2:
                st.success("📝 **Actionable Wellness Plan**")
                st.markdown(wellness_resp.content)
                
            # Export Option
            full_report = f"# Recovery Support Session\n\n## Insights\n{empathy_resp.content}\n\n## Action Plan\n{wellness_resp.content}"
            st.download_button(
                label="📥 Download Session Summary",
                data=full_report,
                file_name="recovery_summary.md",
                mime="text/markdown"
            )
            
        except Exception as e:
            st.error(f"Support process interrupted: {str(e)}")
    else:
        st.warning("⚠️ Please share how you are feeling.")
