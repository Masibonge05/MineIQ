import streamlit as st
from app.components.header import render_header

render_header()
st.title("Model Performance")
st.write("Confusion matrix, R² scores, and precision/recall metrics.")
# TODO(person-2): Implement charts loading from outputs/metrics/
