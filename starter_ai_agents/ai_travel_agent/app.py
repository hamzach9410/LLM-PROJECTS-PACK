import streamlit as st
import os
from datetime import datetime
from agents_config import get_researcher_agent, get_planner_agent
from utils import setup_logger, generate_ics_content

# Initialize logger
logger = setup_logger(__name__)

def init_app():
    """Initialize Streamlit page and session state."""
    st.set_page_config(page_title="🌍 AI Travel Concierge", page_icon="🌍", layout="wide")
    
    if "itinerary" not in st.session_state:
        st.session_state.itinerary = None
    if "travel_history" not in st.session_state:
        st.session_state.travel_history = []
    if "research_done" not in st.session_state:
        st.session_state.research_done = False

def main():
    init_app()
    
    with st.sidebar:
        st.title("🌍 AI Concierge")
        st.markdown("---")
        
        # API Keys
        openai_key = st.text_input("OpenAI API Key", type="password")
        serp_key = st.text_input("SerpAPI Key", type="password")
        
        st.markdown("---")
        if st.button("🗑️ Clear History"):
            st.session_state.travel_history = []
            st.rerun()
            
        st.subheader("📜 Recent Trips")
        if st.session_state.travel_history:
            for trip in st.session_state.travel_history:
                if st.button(f"📍 {trip['dest']} ({trip['days']}d)", key=f"trip_{trip['timestamp']}"):
                    st.session_state.itinerary = trip['itinerary']
                    st.session_state.research_done = True
        else:
            st.caption("No history yet.")

    st.title("🌍 AI Travel Intelligence & Planning")
    st.info("Your autonomous travel team: Researching destinations and planning itineraries on autopilot.")

    # Input Section
    col_in1, col_in2 = st.columns(2)
    destination = col_in1.text_input("Where are we heading?", placeholder="e.g. Kyoto, Japan")
    num_days = col_in2.number_input("Trip Duration (Days)", min_value=1, max_value=30, value=5)

    if st.button("🚀 Generate My Adventure", type="primary", use_container_width=True):
        if not (openai_key and serp_key):
            st.error("Please provide both OpenAI and SerpAPI keys in the sidebar.")
        elif not destination:
            st.warning("Please enter a destination.")
        else:
            try:
                researcher = get_researcher_agent(openai_key, serp_key)
                planner = get_planner_agent(openai_key)
                
                with st.status("🛠️ Travel Team at Work...", expanded=True) as status:
                    st.write("🔍 Researching destinations and activities...")
                    research_results = researcher.run(f"Research {destination} for a {num_days} day trip")
                    
                    st.write("📝 Synthesizing research into itinerary...")
                    prompt = f"""
                    Destination: {destination}
                    Duration: {num_days} days
                    Research Results: {research_results.content}
                    """
                    itinerary_response = planner.run(prompt)
                    
                    st.session_state.itinerary = itinerary_response.content
                    st.session_state.research_done = True
                    
                    # Update History
                    st.session_state.travel_history.append({
                        "dest": destination,
                        "days": num_days,
                        "timestamp": datetime.now().strftime("%H:%M:%S"),
                        "itinerary": st.session_state.itinerary
                    })
                    status.update(label="✅ Itinerary Ready!", state="complete", expanded=False)
                
            except Exception as e:
                st.error(f"Planning failed: {e}")
                logger.exception("Travel Agent Error")

    # Display Results
    if st.session_state.research_done and st.session_state.itinerary:
        st.markdown("---")
        tab1, tab2 = st.tabs(["📄 Itinerary View", "💾 Export & Calendar"])
        
        with tab1:
            st.markdown(st.session_state.itinerary)
            
        with tab2:
            col_ex1, col_ex2 = st.columns(2)
            
            # Markdown Download
            col_ex1.download_button(
                "📥 Download Markdown Report",
                data=st.session_state.itinerary,
                file_name=f"{destination.replace(' ', '_')}_itinerary.md",
                mime="text/markdown",
                use_container_width=True
            )
            
            # ICS Calendar Download
            ics_bytes = generate_ics_content(st.session_state.itinerary)
            col_ex2.download_button(
                "📅 Export to Calendar (.ics)",
                data=ics_bytes,
                file_name=f"{destination.replace(' ', '_')}.ics",
                mime="text/calendar",
                use_container_width=True
            )

if __name__ == "__main__":
    main()
