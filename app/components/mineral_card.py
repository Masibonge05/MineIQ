import streamlit as st

def render_minerals(minerals: dict):
    st.markdown('<div class="mineiq-card">', unsafe_allow_html=True)
    for k, v in minerals.items():
        st.write(f"**{k.capitalize()}**: {v*100:.1f}%")
        st.progress(v)
    st.markdown('</div>', unsafe_allow_html=True)
