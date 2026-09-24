import streamlit as st

def render_confidence(confidence: str):
    conf_class = confidence.lower()
    st.markdown(f'<div class="confidence-badge {conf_class}">Confidence: {confidence}</div>', unsafe_allow_html=True)
