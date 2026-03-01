import streamlit as st
import os
from agents_config import get_analysis_agents
from analysis_engine import AnalysisEngine

# Page configuration
st.set_page_config(
    page_title="Data Intelligence Lab",
    page_icon="🔬",
    layout="wide"
)

st.title("🔬 Autonomous Data Intelligence Lab")
st.markdown("---")

# Sidebar - Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    gemini_key = st.text_input("Gemini API Key", type="password", help="Enter your Google Gemini API Key")
    
    st.divider()
    st.markdown("""
    ### 🧬 Intelligence Pipeline:
    1. **Ingest**: Load structured or raw data.
    2. **Analyze**: Statistical pattern extraction.
    3. **Enrich**: Real-time research integration.
    """)

if not gemini_key:
    st.info("💡 Please enter your Gemini API Key in the sidebar to begin.")
    st.stop()

os.environ["GOOGLE_API_KEY"] = gemini_key

# Initialize Engine and Agents
engine = AnalysisEngine()
analyst, integrator = get_analysis_agents()

# Main Interface
uploaded_file = st.file_uploader("📂 Upload Dataset (CSV)", type="csv")
data_context = st.text_area("Or describe your data findings/patterns:", placeholder="The revenue grew by 20% but the customer churn rate also increased...")

if st.button("🧬 Execute Deep Analysis"):
    if uploaded_file or data_context:
        try:
            with st.status("🏗️ Orchestrating Intelligence Pipeline...", expanded=True) as status:
                input_data = data_context
                if uploaded_file:
                    st.write("📥 Reading dataset...")
                    file_str = uploaded_file.getvalue().decode("utf-8")
                    input_data = engine.load_csv(file_str)
                
                st.write("📊 Extracting internal patterns...")
                internal_report, context_report = engine.analyze_dataset(analyst, integrator, input_data)
                
                status.update(label="✅ Analysis Complete", state="complete", expanded=False)

            col1, col2 = st.columns(2)
            
            with col1:
                st.info("📊 **Internal Analysis**")
                st.markdown(internal_report.content)
            
            with col2:
                st.success("🌐 **Contextual Research**")
                st.markdown(context_report.content)
                
            # Export Option
            full_export = f"# Data Intelligence Report\n\n## Internal Analysis\n{internal_report.content}\n\n## Global Context\n{context_report.content}"
            st.download_button(
                label="📥 Download Full Report",
                data=full_export,
                file_name="intelligence_report.md",
                mime="text/markdown"
            )
            
        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")
    else:
        st.warning("⚠️ Please provide data or a file for analysis.")
