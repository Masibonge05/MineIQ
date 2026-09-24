import streamlit as st
from app.components.header import render_header

render_header()
st.title("Batch Analysis")
st.write("Upload a zip file of images or an HDF5 dataset for batch processing.")
# TODO(person-3): Implement batch processing UI
