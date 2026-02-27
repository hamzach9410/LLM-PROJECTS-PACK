import streamlit as st
import os
import json
from datetime import datetime
from advisor_engine import AdvisorEngine, compute_local_math
from utils import setup_logger, format_currency, safe_number, parse_percentage

# Initialize logger
logger = setup_logger(__name__)

def init_app():
    """Setup page config and session state."""
    st.set_page_config(page_title="🛡️ AI Life Insurance Advisor", page_icon="🛡️", layout="wide")
    
    if 'advisory_history' not in st.session_state:
        st.session_state.advisory_history = []
    
    # Cache for API Keys
    for key in ["openai_api_key", "firecrawl_api_key", "e2b_api_key"]:
        if key not in st.session_state:
            st.session_state[key] = os.getenv(key.upper(), "")

def main():
    init_app()
    
    with st.sidebar:
        st.title("🛡️ Advisor Config")
        st.markdown("---")
        
        # API Keys
        st.session_state.openai_api_key = st.text_input("OpenAI API Key", value=st.session_state.openai_api_key, type="password")
        st.session_state.firecrawl_api_key = st.text_input("Firecrawl API Key", value=st.session_state.firecrawl_api_key, type="password")
        st.session_state.e2b_api_key = st.text_input("E2B API Key", value=st.session_state.e2b_api_key, type="password")
        
        st.markdown("---")
        model_id = st.selectbox("Intelligence Level", ["gpt-4o", "gpt-4o-mini"])
        
        if st.button("🗑️ Clear My Reports"):
            st.session_state.advisory_history = []
            st.rerun()
            
        st.subheader("📜 Recent Reports")
        if st.session_state.advisory_history:
            for report in st.session_state.advisory_history:
                with st.expander(f"📌 {report['time']} - {report['profile']['location']}"):
                    st.write(f"Recommended: {format_currency(report['data']['coverage_amount'], report['data']['coverage_currency'])}")
        else:
            st.caption("No reports generated today.")

    st.title("🛡️ Life Insurance Intelligence Studio")
    st.info("Autonomous advisory combining deterministic financial math with real-time market research.")

    # User Profile Section
    st.subheader("👤 Client Profile")
    with st.container():
        c1, c2, c3 = st.columns(3)
        with c1:
            age = st.number_input("Age", 18, 90, 35)
            annual_income = st.number_input("Annual Income", 0.0, 10000000.0, 75000.0, 5000.0)
            location = st.text_input("Location", "United States")
        with c2:
            dependents = st.number_input("Dependents", 0, 10, 2)
            total_debt = st.number_input("Total Debt (Incl. Mortgage)", 0.0, 50000000.0, 250000.0, 10000.0)
            currency = st.selectbox("Currency", ["USD", "EUR", "GBP", "CAD", "AUD", "INR"])
        with c3:
            savings = st.number_input("Liquid Savings", 0.0, 50000000.0, 50000.0, 5000.0)
            existing_cover = st.number_input("Existing Cover", 0.0, 50000000.0, 0.0, 10000.0)
            horizon = st.select_slider("Income Replacement (Years)", options=[5, 10, 15, 20, 25], value=15)

    profile = {
        "age": age, "annual_income": annual_income, "dependents": dependents,
        "location": location, "total_debt": total_debt, "available_savings": savings,
        "existing_life_insurance": existing_cover, "income_replacement_years": horizon,
        "currency": currency, "request_timestamp": datetime.now().isoformat()
    }

    if st.button("🚀 Generate Professional Assessment", type="primary", use_container_width=True):
        if not all([st.session_state.openai_api_key, st.session_state.firecrawl_api_key, st.session_state.e2b_api_key]):
            st.error("Missing API keys in the sidebar.")
        else:
            try:
                engine = AdvisorEngine(
                    st.session_state.openai_api_key,
                    st.session_state.firecrawl_api_key,
                    st.session_state.e2b_api_key,
                    model_id
                )
                
                with st.status("🕵️ Advisor active...", expanded=True) as status:
                    st.write("🧮 Running deterministic math in sandbox...")
                    report_data = engine.generate_assessment(profile)
                    
                    if report_data:
                        report_entry = {
                            "time": datetime.now().strftime("%H:%M:%S"),
                            "profile": profile,
                            "data": report_data
                        }
                        st.session_state.advisory_history.insert(0, report_entry)
                        st.session_state.active_report = report_entry
                        status.update(label="✅ Assessment Ready!", state="complete", expanded=False)
                    else:
                        st.error("Engine failed to generate data.")
                        
            except Exception as e:
                st.error(f"Advisory failure: {e}")
                logger.exception("Final App Error")

    # Display Active Result
    if hasattr(st.session_state, 'active_report'):
        report = st.session_state.active_report
        data = report['data']
        
        st.markdown("---")
        st.header(f"💼 Coverage Recommendation: {format_currency(data['coverage_amount'], data['coverage_currency'])}")
        
        tab1, tab2, tab3 = st.tabs(["📊 Breakdown", "🏥 Market Options", "📜 Raw JSON"])
        
        with tab1:
            # Local Math verification
            assumptions = data.get("assumptions", {})
            real_rate = parse_percentage(assumptions.get("real_discount_rate", "2%"))
            local_math = compute_local_math(profile, real_rate)
            
            st.subheader("Deterministic Math Verification")
            col1, col2 = st.columns(2)
            with col1:
                st.table({
                    "Component": ["Discounted Income", "Debt Obligations", "Assets Offset"],
                    "Amount": [
                        format_currency(local_math['discounted_income'], currency),
                        format_currency(local_math['debt'], currency),
                        format_currency(local_math['assets_offset'], currency)
                    ]
                })
            with col2:
                st.metric("Final Recommendation", format_currency(local_math['recommended'], currency))
                st.caption(f"Based on {horizon}yr replacement and {real_rate*100}% discount rate.")
            
        with tab2:
            recs = data.get("recommendations", [])
            if recs:
                for r in recs:
                    st.markdown(f"**{r.get('name')}**")
                    st.write(r.get('summary'))
                    if r.get('link'): st.link_button("View Details", r['link'])
                    st.markdown("---")
            else:
                st.write("No specific products surfaced. Consult a local broker.")
        
        with tab3:
            st.json(data)
            st.download_button(
                "📥 Download Report (JSON)",
                data=json.dumps(report, indent=2),
                file_name=f"insurance_report_{report['time'].replace(':','')}.json",
                mime="application/json"
            )

if __name__ == "__main__":
    main()
