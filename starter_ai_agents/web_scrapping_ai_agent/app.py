import streamlit as st
import json
import os
import pandas as pd
from scraper_engine import ScraperEngine
from config import PROVIDERS
from utils import setup_logger, clean_scrape_result, convert_to_csv

# Initialize logger
logger = setup_logger(__name__)

def init_session():
    """Initialize session state for settings and history."""
    if 'scrape_history' not in st.session_state:
        st.session_state.scrape_history = []
    if 'openai_key' not in st.session_state:
        st.session_state.openai_key = os.getenv("OPENAI_API_KEY", "")

def sidebar_setup():
    """Configure sidebar with provider and model settings."""
    with st.sidebar:
        st.title("⚙️ Scraper Settings")
        st.markdown("---")
        
        provider = st.selectbox("LLM Provider", options=list(PROVIDERS.keys()))
        
        api_key = None
        base_url = None
        
        if provider == "OpenAI":
            api_key = st.text_input("OpenAI API Key", value=st.session_state.openai_key, type="password")
            if api_key:
                st.session_state.openai_key = api_key
        
        model_options = PROVIDERS[provider]["models"]
        model = st.selectbox("Select Model", options=model_options)
        
        if provider == "Ollama (Local)":
            base_url = st.text_input("Ollama URL", value=PROVIDERS[provider]["base_url"])

        st.markdown("---")
        if st.button("🗑️ Clear History"):
            st.session_state.scrape_history = []
            st.rerun()
            
    return provider, api_key, model, base_url

def main():
    st.set_page_config(page_title="Scraping Intelligence AI", page_icon="🕵️‍♂️", layout="wide")
    init_session()
    provider, api_key, model, base_url = sidebar_setup()

    st.title("🕵️‍♂️ Scraping Intelligence AI Agent")
    st.info("I help you extract structured data from any website using local or cloud LLMs.")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### 🌐 Target URL")
        url = st.text_input("", placeholder="https://example.com", label_visibility="collapsed")
        
        st.markdown("### ✍️ Extraction Prompt")
        prompt = st.text_area("", placeholder="List all products and their prices as a JSON array...", label_visibility="collapsed")

    with col2:
        st.markdown("### 📋 Extraction Tips")
        st.caption("- Be specific about the fields you want.")
        st.caption("- Mention desired format (e.g., 'as a list of dictionaries').")
        st.caption("- Use local models for private or simple sites.")

    if st.button("🔍 Start Extraction", type="primary"):
        if provider == "OpenAI" and not api_key:
            st.error("Please provide an OpenAI API Key in the sidebar.")
        elif not url or not prompt:
            st.warning("Please provide both a URL and an extraction prompt.")
        else:
            try:
                with st.spinner(f"Agent is analyzing and scraping {url} using {model}..."):
                    engine = ScraperEngine(provider, api_key, model, base_url)
                    raw_result = engine.run(url, prompt)
                    result = clean_scrape_result(raw_result)
                    
                    st.session_state.scrape_history.append({
                        "url": url,
                        "data": result,
                        "timestamp": pd.Timestamp.now().strftime("%H:%M:%S")
                    })

                st.markdown("---")
                st.success("✅ Extraction Successful!")
                
                res_col1, res_col2 = st.columns([2, 1])
                
                with res_col1:
                    st.markdown("### 📦 Extracted Data")
                    st.json(result)
                
                with res_col2:
                    st.markdown("### 📥 Export Options")
                    json_str = json.dumps(result, indent=2)
                    st.download_button("📥 Download JSON", data=json_str, file_name="scrape_result.json", mime="application/json")
                    
                    csv_data = convert_to_csv(result)
                    if csv_data:
                        st.download_button("📥 Download CSV", data=csv_data, file_name="scrape_result.csv", mime="text/csv")
                    
                    md_data = f"## Scrape Result for {url}\n\n```json\n{json_str}\n```"
                    st.download_button("📝 Download MD", data=md_data, file_name="scrape_result.md", mime="text/markdown")

            except Exception as e:
                st.error(f"Scraping failed: {e}")
                logger.exception("Scrape error")

    if st.session_state.scrape_history:
        st.markdown("---")
        st.markdown("### 📜 Session History")
        for h in reversed(st.session_state.scrape_history):
            with st.expander(f"📍 {h['url']} [{h['timestamp']}]"):
                st.json(h['data'])

if __name__ == "__main__":
    main()
