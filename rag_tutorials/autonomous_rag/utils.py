import streamlit as st
import os

def get_db_url():
    """Retrieve database URL from environment or default."""
    return os.getenv("DATABASE_URL", "postgresql+psycopg://ai:ai@localhost:5532/ai")

def apply_autonomous_style():
    """Apply premium aesthetic styling."""
    st.markdown("""
        <style>
        .stAlert {
            border-radius: 12px;
        }
        .main {
            background-color: #ffffff;
        }
        </style>
    """, unsafe_content_type=True)
