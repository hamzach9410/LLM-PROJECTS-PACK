import streamlit as st
import os
from datetime import datetime
from agents_config import get_regular_agent, get_reasoning_agent
from utils import setup_logger, Timer, format_metrics

# Initialize logger
logger = setup_logger(__name__)

def init_session():
    """Setup session state for history and API keys."""
    if 'reasoning_history' not in st.session_state:
        st.session_state.reasoning_history = []
    if 'openai_api_key' not in st.session_state:
        st.session_state.openai_api_key = os.getenv("OPENAI_API_KEY", "")

def main():
    st.set_page_config(page_title="🧠 Reasoning Intelligence Lab", layout="wide", page_icon="🧠")
    init_session()

    with st.sidebar:
        st.title("🧠 Logic Config")
        st.markdown("---")
        
        api_key = st.text_input("OpenAI API Key", value=st.session_state.openai_api_key, type="password")
        if api_key:
            st.session_state.openai_api_key = api_key
            os.environ["OPENAI_API_KEY"] = api_key

        model_standard = st.selectbox("Standard Model", ["gpt-4o-mini", "gpt-3.5-turbo"])
        model_reasoning = st.selectbox("Reasoning Model", ["gpt-4o", "o1-preview"])
        
        st.markdown("---")
        if st.button("🗑️ Clear History"):
            st.session_state.reasoning_history = []
            st.rerun()

        st.subheader("📜 Recent Analysis")
        if st.session_state.reasoning_history:
            for entry in st.session_state.reasoning_history:
                if st.button(f"🔍 {entry['query'][:20]}...", key=f"hist_{entry['time']}"):
                    st.session_state.active_entry = entry
        else:
            st.caption("No history yet.")

    st.title("🧠 AI Reasoning Intelligence Lab")
    st.info("Side-by-side comparison of standard vs advanced reasoning models. Deep dive into the 'Thought Process'.")

    # Input Area
    query = st.text_input("Enter a complex question or logic puzzle:", placeholder="e.g. How many 'r' are in 'supercalifragilisticexpialidocious'?")
    
    if st.button("🚀 Run Comparative Analysis", type="primary", use_container_width=True):
        if not st.session_state.openai_api_key:
            st.error("Please provide an OpenAI API Key in the sidebar.")
        elif not query:
            st.warning("Please enter a query.")
        else:
            try:
                reg_agent = get_regular_agent(st.session_state.openai_api_key, model_standard)
                reas_agent = get_reasoning_agent(st.session_state.openai_api_key, model_reasoning)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader(f"⚡ Standard ({model_standard})")
                    with st.spinner("Thinking..."):
                        with Timer() as t:
                            reg_res = reg_agent.run(query)
                        reg_metrics = format_metrics(t.interval, reg_res)
                        st.markdown(reg_res.content)
                        st.caption(f"⏱️ Latency: {reg_metrics['latency_sec']}s")

                with col2:
                    st.subheader(f"🧠 Reasoning ({model_reasoning})")
                    with st.spinner("Reasoning step-by-step..."):
                        with Timer() as t:
                            reas_res = reas_agent.run(query, show_full_reasoning=True)
                        reas_metrics = format_metrics(t.interval, reas_res)
                        st.markdown(reas_res.content)
                        st.caption(f"⏱️ Latency: {reas_metrics['latency_sec']}s")
                
                # Update History
                entry = {
                    "query": query,
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "standard": {"content": reg_res.content, "metrics": reg_metrics},
                    "reasoning": {"content": reas_res.content, "metrics": reas_metrics}
                }
                st.session_state.reasoning_history.append(entry)
                st.session_state.active_entry = entry
                
            except Exception as e:
                st.error(f"Analysis failed: {e}")
                logger.exception("Reasoning Engine Error")

    # Display Active Entry from History if selected
    if hasattr(st.session_state, 'active_entry') and not st.session_state.get('last_run_query') == query:
        entry = st.session_state.active_entry
        st.markdown("---")
        st.subheader(f"Review: {entry['query']}")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(entry['standard']['content'])
            st.caption(f"Latency: {entry['standard']['metrics']['latency_sec']}s")
        with c2:
            st.markdown(entry['reasoning']['content'])
            st.caption(f"Latency: {entry['reasoning']['metrics']['latency_sec']}s")
            
        # Export (Contribution 17)
        export_text = f"# Reasoning Comparison\n\n## Query\n{entry['query']}\n\n## Standard Response\n{entry['standard']['content']}\n\n## Reasoning Response\n{entry['reasoning']['content']}"
        st.download_button("📥 Download This Comparison (MD)", data=export_text, file_name=f"reasoning_{entry['time']}.md")

if __name__ == "__main__":
    main()
