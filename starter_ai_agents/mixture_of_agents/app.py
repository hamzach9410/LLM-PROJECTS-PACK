import streamlit as st
import asyncio
import os
from agents_config import get_moa_agents
from moa_engine import MOAEngine
from utils import apply_custom_style, logger

# Page configuration
st.set_page_config(
    page_title="MOA Intelligence Hub",
    page_icon="🧠",
    layout="wide"
)

apply_custom_style()

st.title("🧠 Mixture-of-Agents Hub")
st.markdown("---")

# Sidebar - Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Together API Key", type="password", help="Enter your Together AI API Key")
    
    st.divider()
    st.markdown("""
    ### 🔬 Methodology:
    1. **Query**: Request sent to 4 diverse models.
    2. **Synthesis**: Candidate responses analyzed.
    3. **Aggregate**: High-fidelity final report generated.
    """)

if not api_key:
    st.info("💡 Please enter your Together API Key in the sidebar to begin.")
    st.stop()

# Initialize Engine
engine = MOAEngine(api_key=api_key)
ref_models, aggregator = get_moa_agents()

# Main Interface
user_prompt = st.text_area("What would you like to investigate?", placeholder="Analyze the impact of quantum computing on modern cryptography...")

if st.button("🚀 Execute Collaborative Analysis"):
    if user_prompt:
        try:
            with st.status("🏗️ Orchestrating Multi-Model Analysis...", expanded=True) as status:
                # Step 1: Run reference models
                st.write("📡 Calling reference models...")
                reference_results = asyncio.run(engine.get_reference_responses(ref_models, user_prompt))
                
                # Step 2: Show individual results in expanders
                st.write("📊 Evaluating candidate perspectives...")
                for model, resp in reference_results:
                    with st.expander(f"Insight from {model}"):
                        st.write(resp)
                
                # Step 3: Run Aggregator
                st.write("🧠 Synthesizing final intelligence report...")
                final_response = engine.aggregate_responses(aggregator, reference_results, user_prompt)
                
                status.update(label="✅ Analysis Complete", state="complete", expanded=False)

            st.subheader("🏁 Final Synthesized Intelligence")
            st.markdown(final_response.content)
            
            # Export Option
            st.download_button(
                label="📥 Download Intelligence Report",
                data=final_response.content,
                file_name="moa_report.md",
                mime="text/markdown"
            )
            
        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")
            logger.error(f"Error during MOA execution: {e}")
    else:
        st.warning("⚠️ Please enter a question to analyze.")
