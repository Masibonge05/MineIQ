import streamlit as st
import base64
import os

def render_header():
    # Helper to load images to base64
    def load_image_base64(path):
        if not os.path.exists(path):
            return ""
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    # Load logos
    mineiq_logo = load_image_base64("assets/logo.svg")
    
    # Try to load the user's pasted Mintek logo
    mintek_logo = load_image_base64("assets/mintek-logo.png")
    
    mintek_img_tag = ""
    if mintek_logo:
        mintek_img_tag = f'<img src="data:image/png;base64,{mintek_logo}" height="56"/>'
    else:
        # Fallback to the SVG if the PNG isn't there yet
        mintek_svg = load_image_base64("assets/mintek-logo.svg")
        mintek_img_tag = f'<img src="data:image/svg+xml;base64,{mintek_svg}" height="56"/>'

    st.markdown(f"""
    <div class="mineiq-header" style="justify-content: space-between;">
      <div style="display: flex; align-items: center; gap: 1rem;">
          <img src="data:image/svg+xml;base64,{mineiq_logo}" height="48"/>
      </div>
      <div>
          {mintek_img_tag}
      </div>
    </div>
    """, unsafe_allow_html=True)
