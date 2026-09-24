import os
import base64

BASE_DIR = r"c:\Users\shaba\Documents\mintek"

def encode_file(path):
    with open(os.path.join(BASE_DIR, path), "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

logo_base64 = encode_file("assets/logo.svg")
mintek_base64 = encode_file("assets/mintek-logo.svg")

header_content = f"""import streamlit as st

def render_header():
    mintek_logo = "{mintek_base64}"
    mineiq_logo = "{logo_base64}"
    
    st.markdown(f\"\"\"
    <div class="mineiq-header" style="justify-content: space-between;">
      <div style="display: flex; align-items: center; gap: 1rem;">
          <img src="data:image/svg+xml;base64,{{mineiq_logo}}" height="48"/>
      </div>
      <div>
          <img src="data:image/svg+xml;base64,{{mintek_logo}}" height="48"/>
      </div>
    </div>
    \"\"\", unsafe_allow_html=True)
"""

with open(os.path.join(BASE_DIR, "app/components/header.py"), "w", encoding="utf-8") as f:
    f.write(header_content)
