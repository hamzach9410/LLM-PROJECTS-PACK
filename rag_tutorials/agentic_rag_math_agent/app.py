import streamlit as st
import pandas as pd
import json
import os
from rag.query_router import answer_math_question
from app.benchmark import benchmark_math_agent
from data.load_gsm8k_data import load_jeebench_dataset

# Premium UI Styling
st.set_page_config(page_title="Math Intel Lab", page_icon="🧮", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #fcfcfc; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #f0f2f6; border-radius: 4px 4px 0px 0px; gap: 1px; padding-top: 10px; padding-bottom: 10px; }
    .stTabs [aria-selected="true"] { background-color: #2b6cb0; color: white; }
    </style>
""", unsafe_content_type=True)

st.title("🧮 Global Math Intelligence & Research Lab")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["🚀 Research Assistant", "📁 Feedback Vault", "📊 Strategic Benchmarking"])

# Tab 1: Assistant
with tab1:
    st.subheader("🧪 Advanced Mathematical Reasoning")
    st.info("Ask complex JEE-level math questions. The agent utilizes agentic-RAG with autonomous routing and guardrails.")
    
    if "last_q" not in st.session_state: st.session_state.last_q = ""
    if "last_a" not in st.session_state: st.session_state.last_a = ""
    
    query = st.text_input("Mathematical Hypothesis / Query:", placeholder="e.g., Integrate exp(x)*cos(x) from 0 to pi...")
    
    if st.button("Execute Reasoning Cycle"):
        if query:
            with st.spinner("Synthesizing step-by-step mathematical proof..."):
                ans = answer_math_question(query)
                st.session_state.last_q = query
                st.session_state.last_a = ans
                st.session_state.feedback_done = False
                
    if st.session_state.last_a:
        st.markdown("### 📝 Proof & Synthesis")
        st.success(st.session_state.last_a)
        
        # Human-in-the-loop
        st.divider()
        st.caption("Human-in-the-loop: Rate this synthesis for correctness.")
        c1, c2 = st.columns([0.1, 0.9])
        with c1: 
            if st.button("👍"): st.toast("Positive feedback logged.")
        with c2:
            if st.button("👎"): st.toast("Negative feedback logged.")

# Tab 2: Feedback
with tab2:
    st.subheader("🗄️ Intelligence Logs")
    log_path = "logs/feedback_log.json"
    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            logs = json.load(f)
        st.dataframe(pd.DataFrame(logs), use_container_width=True)
    else:
        st.info("No intelligence logs recorded yet.")

# Tab 3: Benchmark
with tab3:
    st.subheader("🏁 Performance Benchmarking")
    dataset = load_jeebench_dataset()
    st.caption(f"Connected to JEEBench Intelligence Dataset ({len(dataset)} entries)")
    
    limit = st.slider("Samples for benchmarking", 5, 50, 10)
    if st.button("Run Performance Audit"):
        with st.spinner(f"Audit in progress: Testing {limit} samples..."):
            df, acc = benchmark_math_agent(limit=limit)
            st.metric("Aggregate Accuracy", f"{acc:.2f}%")
            st.dataframe(df, use_container_width=True)
