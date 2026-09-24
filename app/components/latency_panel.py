import streamlit as st

def render_latency(latency_ms: int):
    st.caption(f"Latency: {latency_ms}ms")
