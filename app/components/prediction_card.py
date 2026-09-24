import streamlit as st

def render_prediction(predictions: dict):
    st.markdown('<div class="mineiq-card">', unsafe_allow_html=True)
    for k, v in predictions.items():
        val = v['value']
        low = v['low']
        high = v['high']
        st.write(f"**{k}**: {val:.1f} (90% CI: {low:.1f} - {high:.1f})")
    st.markdown('</div>', unsafe_allow_html=True)
