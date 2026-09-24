import streamlit as st
import os

st.set_page_config(page_title="MineIQ | Mintek", page_icon="assets/favicon.svg", layout="wide")

def load_css():
    with open("app/theme/styles.css", "r") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css()

st.title("MineIQ")
st.write("Welcome to the MineIQ Dashboard.")
st.write("Please select a page from the sidebar to begin.")
