import streamlit as st
import os
from agents_config import get_visualisation_agents
from visualisation_engine import VisualisationEngine

# Page configuration
st.set_page_config(
    page_title="Visual Intelligence Lab",
    page_icon="🎨",
    layout="wide"
)

st.title("🎨 Visual Data Intelligence Hub")
st.markdown("---")

# Sidebar - Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    gemini_key = st.text_input("Gemini API Key", type="password", help="Enter your Google Gemini API Key")
    
    st.divider()
    st.markdown("""
    ### 📊 Visual Pipeline:
    1. **Blueprint**: AI selects optimal chart types.
    2. **Design**: Layout and aesthetic planning.
    3. **Narrative**: Storyboarding the data journey.
    """)

if not gemini_key:
    st.info("💡 Please enter your Gemini API Key in the sidebar to begin.")
    st.stop()

os.environ["GOOGLE_API_KEY"] = gemini_key

# Initialize Engine and Agents
engine = VisualisationEngine()
specialist, designer = get_visualisation_agents()

# Main Interface
uploaded_file = st.file_uploader("📂 Upload Data for Viz (CSV)", type="csv")
viz_context = st.text_area("Or describe the trends you want to visualize:", placeholder="We have monthly sales data for 2024 showing a peak in December...")

if st.button("🎨 Design Visual Story"):
    if uploaded_file or viz_context:
        try:
            with st.status("🏗️ Architecting Visual Strategy...", expanded=True) as status:
                input_data = viz_context
                if uploaded_file:
                    st.write("📥 Processing dataset...")
                    file_str = uploaded_file.getvalue().decode("utf-8")
                    input_data = engine.load_data_preview(file_str)
                
                st.write("📐 Blueprinting visualizations...")
                blueprint, story = engine.blueprint_visuals(specialist, designer, input_data)
                
                status.update(label="✅ Design Complete", state="complete", expanded=False)

            col1, col2 = st.columns(2)
            
            with col1:
                st.info("📐 **Viz Blueprint**")
                st.markdown(blueprint.content)
            
            with col2:
                st.success("📝 **Data Narrative**")
                st.markdown(story.content)
                
            # Export Option
            full_design = f"# Visual Intelligence Blueprint\n\n## chart Recommendations\n{blueprint.content}\n\n## Data Story\n{story.content}"
            st.download_button(
                label="📥 Download Design Blueprint",
                data=full_design,
                file_name="viz_blueprint.md",
                mime="text/markdown"
            )
            
        except Exception as e:
            st.error(f"Design failed: {str(e)}")
    else:
        st.warning("⚠️ Please provide data or a description for visualization.")
