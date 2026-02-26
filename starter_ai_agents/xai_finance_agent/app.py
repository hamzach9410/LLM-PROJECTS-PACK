import streamlit as st
import os
import pandas as pd
from datetime import datetime
from agents_config import get_xai_finance_agent
from finance_engine import FinanceEngine
from utils import setup_logger, format_currency, format_percentage

# Initialize logger
logger = setup_logger(__name__)

def init_session():
    """Initialize session state for settings and watchlist."""
    if 'watchlist' not in st.session_state:
        st.session_state.watchlist = []
    if 'xai_api_key' not in st.session_state:
        st.session_state.xai_api_key = os.getenv("XAI_API_KEY", "")

def main():
    st.set_page_config(page_title="💹 xAI Finance Dashboard", layout="wide")
    init_session()

    with st.sidebar:
        st.title("💹 Dashboard Settings")
        st.markdown("---")
        
        # API Configuration
        api_key = st.text_input("xAI API Key", value=st.session_state.xai_api_key, type="password")
        if api_key:
            st.session_state.xai_api_key = api_key
            os.environ["XAI_API_KEY"] = api_key

        st.markdown("---")
        # Model Selection (Contribution 11)
        model_choice = st.selectbox("Narrator Model", ["grok-4-1-fast", "grok-beta"], index=0)
        
        # Portfolio Watchlist (Contribution 15)
        st.markdown("### ⭐ My Watchlist")
        if st.session_state.watchlist:
            for ticker in st.session_state.watchlist:
                col1, col2 = st.columns([3, 1])
                col1.write(f"**{ticker}**")
                if col2.button("🗑️", key=f"del_{ticker}"):
                    st.session_state.watchlist.remove(ticker)
                    st.rerun()
        else:
            st.caption("No tickers added yet.")

    st.title("💹 xAI Financial Intelligence Dashboard")
    st.info("Powered by xAI Grok. Real-time market data, technical analysis, and sentiment.")

    # Main Inputs
    col_in1, col_in2 = st.columns([3, 1])
    ticker_input = col_in1.text_input("Enter Stock Ticker (e.g. TSLA, AAPL, BTC-USD)", placeholder="TSLA").upper()
    
    if ticker_input and ticker_input not in st.session_state.watchlist:
        if col_in2.button("➕ Add to Watchlist"):
            st.session_state.watchlist.append(ticker_input)

    tabs = st.tabs(["🔍 Analysis", "📊 Market Overview", "📈 Charts"])

    with tabs[0]:
        if st.button("🚀 Analyze Market Intelligence", type="primary"):
            if not st.session_state.xai_api_key:
                st.error("Please enter your xAI API Key in the sidebar.")
            elif not ticker_input:
                st.warning("Please enter a stock ticker.")
            else:
                try:
                    with st.spinner(f"Agent generating technical report for {ticker_input}..."):
                        # Fetch Quick Data for Metrics
                        eng = FinanceEngine()
                        data = eng.get_stock_info(ticker_input)
                        
                        if data:
                            st.markdown(f"## {data['name']} ({ticker_input})")
                            m1, m2, m3 = st.columns(3)
                            m1.metric("Current Price", format_currency(data['price']), format_percentage(data['change_pct']))
                            m2.metric("Market Cap", f"${data['market_cap'] / 1e9:,.2f}B" if data['market_cap'] else "N/A")
                            m3.metric("P/E Ratio", f"{data['pe_ratio']:.2f}" if data['pe_ratio'] else "N/A")

                        # Agent Analysis
                        agent = get_xai_finance_agent(st.session_state.xai_api_key, model_id=model_choice)
                        response = agent.run(f"Perform a detailed technical and sentiment analysis for {ticker_input}. Focus on recent news and technical indicators.")
                        
                        st.markdown("### 📋 Agent Intelligence Report")
                        st.markdown(response.content)
                        
                        # Export Button (Contribution 17)
                        export_md = f"# Technical Report: {ticker_input}\nDate: {datetime.now().strftime('%Y-%m-%d')}\n\n{response.content}"
                        st.download_button("📥 Export Report (MD)", data=export_md, file_name=f"{ticker_input}_analysis.md")

                except Exception as e:
                    st.error(f"Analysis Failed: {e}")
                    logger.exception("Agent run error")

    with tabs[1]:
        st.markdown("### 🌎 Global Market Pulse")
        # Sample News Analysis logic or comparison
        st.caption("Comparison and multi-ticker analysis section.")
        compare_tickers = st.multiselect("Select Tickers to Compare", ["TSLA", "AAPL", "NVDA", "BTC-USD", "ETH-USD"], default=["TSLA", "NVDA"])
        if st.button("⚖️ Compare Performance"):
             # Add side-by-side metric comparison logic here
             st.write("Coming soon: Multi-ticker performance table.")

    with tabs[2]:
        if ticker_input:
            st.markdown(f"### 📈 {ticker_input} Price History")
            hist = FinanceEngine.get_price_history(ticker_input)
            if hist is not None:
                st.line_chart(hist['Close'])
            else:
                st.write("Could not load charts for this ticker.")
        else:
            st.info("Enter a ticker to view interactive charts.")

if __name__ == "__main__":
    main()
