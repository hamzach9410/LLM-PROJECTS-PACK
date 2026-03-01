import streamlit as st
from agents_config import get_podcast_agents
from podcast_engine import ContentEngine
import os

# Page configuration
st.set_page_config(
    page_title="Podcast Engine",
    page_icon="🎙️",
    layout="wide"
)

st.title("🎙️ Blog-to-Podcast Engine")
st.markdown("---")

# Sidebar - Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    gemini_key = st.text_input("Gemini API Key", type="password", help="Enter your Google Gemini API Key")
    
    st.divider()
    st.markdown("""
    ### 🔄 Process:
    1. **Scrape**: Extraction of blog text.
    2. **Analyze**: AI identifies core insights.
    3. **Rewrite**: Script generated for audio.
    """)

if not gemini_key:
    st.info("💡 Please enter your Gemini API Key in the sidebar to begin.")
    st.stop()

os.environ["GOOGLE_API_KEY"] = gemini_key

# Initialize Engine and Agents
engine = ContentEngine()
analyst, writer = get_podcast_agents()

# Main Interface
blog_url = st.text_input("🔗 Blog URL", placeholder="https://example.com/blog-post")

if st.button("📻 Generate Podcast Script"):
    if blog_url:
        try:
            with st.status("🛠️ Processing Content...", expanded=True) as status:
                st.write("🌐 Scraping blog content...")
                blog_text = engine.scrape_blog(blog_url)
                
                st.write("🧠 Analyzing insights...")
                # The engine handles the analysis and scriptwriting
                final_script = engine.transform_to_script(analyst, writer, blog_text)
                
                status.update(label="✅ Script Generated", state="complete", expanded=False)

            st.subheader("📝 Final Podcast Script")
            st.markdown(final_script.content)
            
            # Export Option
            st.download_button(
                label="📥 Download Script",
                data=final_script.content,
                file_name="podcast_script.md",
                mime="text/markdown"
            )
            
        except Exception as e:
            st.error(f"Transformation failed: {str(e)}")
    else:
        st.warning("⚠️ Please enter a blog URL.")
