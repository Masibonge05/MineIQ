import streamlit as st
from app.components.header import render_header

render_header()
st.title("About MineIQ")

st.markdown("""
### Team
- **Person 1:** Data Lead
- **Person 2:** Mineral AI Lead
- **Person 3:** Process & System Lead

### Acknowledgements
We acknowledge the HIDSAG authors (Ehrenfeld et al., 2023, Scientific Data) for the dataset.
**Citation:** https://doi.org/10.6084/m9.figshare.c.5983921.v1
**HIDSAG GitHub:** https://github.com/alges/hidsag

### Mintek
*South African mineral processing research organisation.*
""")
