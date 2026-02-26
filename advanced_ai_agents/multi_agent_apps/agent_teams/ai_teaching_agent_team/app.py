import streamlit as st
import os
from agents_config import get_teaching_team_agents
from storage_engine import StorageEngine
from utils import setup_logger, extract_google_doc_link

# Initialize logger
logger = setup_logger(__name__)

def init_session():
    """Initialize session state for settings and theory history."""
    if 'topic_history' not in st.session_state:
        st.session_state.topic_history = []
    if 'openai_api_key' not in st.session_state:
        st.session_state.openai_api_key = os.getenv("OPENAI_API_KEY", "")
    if 'composio_api_key' not in st.session_state:
        st.session_state.composio_api_key = os.getenv("COMPOSIO_API_KEY", "")
    if 'serpapi_api_key' not in st.session_state:
        st.session_state.serpapi_api_key = os.getenv("SERPAPI_API_KEY", "")

def main():
    st.set_page_config(page_title="👨‍🏫 AI Teaching Team", layout="wide")
    init_session()

    with st.sidebar:
        st.title("👨‍🏫 Teaching Team Settings")
        st.markdown("---")
        
        with st.expander("🔑 API Keys", expanded=not all([st.session_state.openai_api_key, st.session_state.composio_api_key])):
            st.session_state.openai_api_key = st.text_input("OpenAI Key", value=st.session_state.openai_api_key, type="password")
            st.session_state.composio_api_key = st.text_input("Composio Key", value=st.session_state.composio_api_key, type="password")
            st.session_state.serpapi_api_key = st.text_input("SerpAPI Key", value=st.session_state.serpapi_api_key, type="password")
        
        if st.session_state.topic_history:
            st.markdown("---")
            st.markdown("### 📜 Topic History")
            for t in reversed(st.session_state.topic_history):
                st.button(t, key=f"hist_{t}", on_click=lambda x=t: st.session_state.update({"current_topic": x}))

        if st.button("🗑️ Clear Session"):
            st.session_state.topic_history = []
            st.rerun()

    st.title("👨‍🏫 AI Teaching Agent Team")
    st.markdown("### Your personal academic team for mastering any topic")
    
    topic = st.text_input("What do you want to learn today?", placeholder="e.g. Quantum Computing, LoRA, Docker...")

    if st.button("🚀 Start Learning Session", type="primary"):
        if not all([st.session_state.openai_api_key, st.session_state.composio_api_key, st.session_state.serpapi_api_key]):
            st.error("Please provide all API keys in the sidebar.")
        elif not topic:
            st.warning("Please enter a topic.")
        else:
            try:
                os.environ["OPENAI_API_KEY"] = st.session_state.openai_api_key
                
                # Setup Engines and Agents
                storage = StorageEngine(st.session_state.composio_api_key)
                prof, advisor, librarian, ta = get_teaching_team_agents(
                    st.session_state.openai_api_key, 
                    st.session_state.serpapi_api_key, 
                    storage.get_create_tool()
                )

                # Execution loop
                responses = {}
                agent_list = [
                    ("Professor", prof, "📚 Researching knowledge base..."),
                    ("Academic Advisor", advisor, "🗺️ Designing learning roadmap..."),
                    ("Research Librarian", librarian, "🔍 Curating deep-dive resources..."),
                    ("Teaching Assistant", ta, "📝 Creating practice materials...")
                ]

                progress_bar = st.progress(0)
                for i, (name, agent, msg) in enumerate(agent_list):
                    with st.spinner(msg):
                        res = agent.run(f"Topic: {topic}. Create document and provide link.")
                        responses[name] = res.content
                        progress_bar.progress((i + 1) / len(agent_list))

                # Display Results
                st.markdown("---")
                st.success(f"Learning session for **{topic}** complete!")
                
                # Export Button (Contribution 18)
                export_data = f"# Learning Session: {topic}\n\n"
                for name, content in responses.items():
                    link_id = extract_google_doc_link(content)
                    if link_id:
                        export_data += f"- **{name}**: https://docs.google.com{link_id}\n"
                
                st.download_button("📥 Export All Links (Markdown)", data=export_data, file_name=f"{topic}_session.md")

                # Links Card Section
                st.markdown("### 📝 Generated Study Materials")
                l_cols = st.columns(4)
                for idx, (name, content) in enumerate(responses.items()):
                    with l_cols[idx]:
                        link_id = extract_google_doc_link(content)
                        if link_id:
                            st.link_button(f"📄 {name} Doc", f"https://docs.google.com{link_id}")
                        else:
                            st.warning(f"No link for {name}")

                # Detailed Content
                for name, content in responses.items():
                    with st.expander(f"🔍 {name} Detailed Output"):
                        st.markdown(content)
                
                if topic not in st.session_state.topic_history:
                    st.session_state.topic_history.append(topic)

            except Exception as e:
                st.error(f"An error occurred: {e}")
                logger.exception("Agent execution fail")

if __name__ == "__main__":
    main()
