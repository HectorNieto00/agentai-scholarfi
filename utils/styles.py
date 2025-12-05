# utils/styles.py
import streamlit as st
from pathlib import Path

def load_css(file_name="styles.css"):
    css_path = Path(__file__).parent.parent / "styles" / file_name
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
