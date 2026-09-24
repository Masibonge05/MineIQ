import streamlit as st

def render_decisions(decisions: list):
    for dec in decisions:
        priority = dec['priority'].lower()
        st.markdown(f"""
        <div class="alert {priority}">
            <strong>{dec['priority']}</strong>: {dec['message']}
            <br/><small>{dec['reason']}</small>
        </div>
        """, unsafe_allow_html=True)
